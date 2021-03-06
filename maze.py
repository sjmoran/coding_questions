'''
Sean Moran
sean.j.moran@gmail.com
'''

import numpy as np

class MazeSolver():
    """
    My solution is to convert the maze (boolean matrix) to an adjacency matrix (S)
    that gives for each position ij in the maze S_ij=1 if those positions are 
    adjacent and S_ij=0 if not.

    Matrix multiplying the adjacency matrix several times (by the maximum of the
    x,y distance we can travel in the maze) gives the nodes accessible to a given 
    node in the maze. I term this the accessibility matrix A where A_ij=1 if nodes
    i,j are accessible in the maze, and A_ij=0 otherwise.

    This solution trades off an initial offline pre-processing step (computing 
    the accessibility matrix) for fast querying ~O(1) of node accessibility. This 
    pre-processing takes O(N^3) where N are the number of squares in the maze
    and O(N^2) memory. Sparse matrix data structures could be leveraged to 
    reduce these complexities (we do not need to explicitly store the zeros).

    Assumptions: I assume coordinates are zero indexed (start at zero). So for a
    6x6 square maze, (0,0) is top left of the maze, (0,5) is top-right, (5,0) is 
    bottom left and (5,5) is bottom-right

    i indexes row and j indexes columns
    """

    def __init__(self, grid):
        """Object initialiser

        :param grid: Numpy matrix representing the grid 
        :returns: N/A
        :rtype: N/A

        """

        self.grid=grid
        '''
        Step 1: convert grid to an adjacency matrix A that specifies the local 
        1-hop connectivity of each square in the maze
        '''
        self.adjacency_matrix=self._grid_to_adjacency_matrix()

        print("Adjacency matrix is: \n" + str(self.adjacency_matrix))

        '''
        Step 2: use the adjacency matrix to compute the accessibility matrix.
        We compute the nodes accessible via the maximum number of hops possible
        in maze
        '''
        max_hops=(self.grid.shape[0]*self.grid.shape[1])
        
        self.accessibility_matrix=np.copy(self.adjacency_matrix)
        
        for i in range(0,max_hops):
            '''
            This is the workhorse computing the number of hops that two nodes are away from each other in maze
            0 indicates that the nodes are not reacheable.
            '''
            self.accessibility_matrix=np.matmul(self.accessibility_matrix,self.accessibility_matrix.T)
            self.accessibility_matrix[self.accessibility_matrix>0]=1

            
    def is_connected(self, grid, aX, aY, bX, bY):
        """Public function that checks if two coordinates are reacheable from each other in the maze

        :param grid: Numpy boolean matrix M representing the maze. M_ij=1 indicates a wall, M_ij=0 indicates a path. 
        :param aX: integer specifiying starting x-coordinate of point A 
        :param aY: integer specifiying starting y-coordinate of point A
        :param bX: integer specifiying starting x-coordinate of point B 
        :param bY: integer specifiying starting y-coordinate of point B
        :returns: Boolean indicating reacheablity status between the two points
        :rtype: Boolean

        """
        '''
        Step 3: answer the user query by converting their maze coordinates to
        adjacency matrix coordinates
        '''
        nodeA=self._grid_coords_to_adjacency_coords(aX,aY)
        nodeB=self._grid_coords_to_adjacency_coords(bX,bY)

        if self.accessibility_matrix[nodeA,nodeB]>0:
            return True

        return False

    def _grid_coords_to_adjacency_coords(self, i, j):
        """Takes a coordinate from the maze and converts it to its associated adjacency matrix
        coordinate.

        :param i: x position
        :param j: y position 
        :returns: Adjacency matrix coordinate
        :rtype: Integer
        """
        return (i)*(self.grid.shape[1])+j

    def _get_grid_coord_value(self,i,j):
        """Returns the value from the maze at the current i,j position 

        :param i: x position
        :param j: y position 
        :returns: Value at those coordintes (integer, either 0 or 1)
        :rtype: Integer

        """

        if (i>=0 and i<self.grid.shape[0]):
            if (j>=0 and j<self.grid.shape[1]):
                return(int(self.grid[i,j]))
        return -1
    
    def _grid_to_adjacency_matrix(self):
        """Private function that converts a grid (maze) to the adjacency matrix representation

        For each square in the maze we look at the surrounding 9 squares that are 1 hop away
        from that square.
        
        We add a 1 to the adjacency matrix for a pair of squares if a square is not a wall
        and zero otherwise.

        :returns: numpy matrix representing the 1 hop relationships between maze squares
        :rtype: numpy matrix

        """
        num_nodes=self.grid.shape[0]*self.grid.shape[1]  # each position of the maze is a graph node
        adjacency_matrix=np.zeros((num_nodes,num_nodes)) # build a matrix showing the local connectivity of the nodes

        for i in range(0,self.grid.shape[0]):

            for j in range(0,self.grid.shape[1]):
                '''
                Node1 represents our current position in maze. Nodes 2-9 are the 8 squares surrounding our current 
                position
                '''
                node1=self._grid_coords_to_adjacency_coords(i,j)

                if self._get_grid_coord_value(i,j)==0:

                    adjacency_matrix[node1,node1]=1   # a node is reacheable from itself

                    if self._get_grid_coord_value(i+1,j)==0:
                        node2=self._grid_coords_to_adjacency_coords(i+1,j) # look at square below
                        adjacency_matrix[node1,node2]=1
                        adjacency_matrix[node2,node1]=1

                    if self._get_grid_coord_value(i+1,j-1)==0:     
                        node3=self._grid_coords_to_adjacency_coords(i+1,j-1) # look at square below and to the left
                        adjacency_matrix[node1,node3]=1
                        adjacency_matrix[node3,node1]=1

                    if self._get_grid_coord_value(i+1,j+1)==0:
                        node4=self._grid_coords_to_adjacency_coords(i+1,j+1) # look at square below and to the right
                        adjacency_matrix[node1,node4]=1
                        adjacency_matrix[node4,node1]=1

                    if self._get_grid_coord_value(i-1,j)==0:     
                        node5=self._grid_coords_to_adjacency_coords(i-1,j) # look at square above 
                        adjacency_matrix[node1,node5]=1
                        adjacency_matrix[node5,node1]=1

                    if self._get_grid_coord_value(i-1,j+1)==0:     
                        node6=self._grid_coords_to_adjacency_coords(i-1,j+1) # look at square above and to the right
                        adjacency_matrix[node1,node6]=1
                        adjacency_matrix[node6,node1]=1

                    if self._get_grid_coord_value(i-1,j-1)==0:     
                        node7=self._grid_coords_to_adjacency_coords(i-1,j-1) # look at square above and to the left
                        adjacency_matrix[node1,node7]=1
                        adjacency_matrix[node7,node1]=1

                    if self._get_grid_coord_value(i,j+1)==0:     
                        node8=self._grid_coords_to_adjacency_coords(i,j+1) # look at square the right
                        adjacency_matrix[node1,node8]=1
                        adjacency_matrix[node8,node1]=1

                    if self._get_grid_coord_value(i,j-1)==0:     
                        node9=self._grid_coords_to_adjacency_coords(i,j-1) # look at square to the left
                        adjacency_matrix[node1,node9]=1
                        adjacency_matrix[node9,node1]=1
                        
        return adjacency_matrix
    
def main():
    """Main function containing some unit tests

    :returns: N/A
    :rtype: N/A

    """

    '''
    Some unit tests to check algorithm works correctly
    '''
    grid1=np.zeros((3,3))

    grid1[0,1]=1
    grid1[1,1]=1
    grid1[2,1]=1
    
    print("Maze is: \n" + str(grid1))
    solver1=MazeSolver(grid1)
 
    is_connected1=solver1.is_connected(grid1,0,0,2,2)
    assert(is_connected1==False)
    
    print("Coordinates 0,0 and 2,2 are connected: " + str(is_connected1))

    '''
    Grid2 is grid1 but we remove a part of the wall blocking access between
    (0,0) and (2,2)
    '''
    grid2=np.zeros((3,3))

    grid2[0,1]=1
    grid2[1,1]=1
    grid2[2,1]=0
    
    print("Maze2 is: \n" + str(grid2))
    solver2=MazeSolver(grid2)
 
    is_connected2=solver2.is_connected(grid2,0,0,2,2)
    
    print("Coordinates 0,0 and 2,2 are connected: " + str(is_connected2))
    assert(is_connected2==True)

    '''
    Grid3 is the actual example from the coding test question
    '''
    grid3=np.zeros((9,13))

    grid3[0,0]=1
    grid3[1,0]=1
    grid3[5,0]=1
    grid3[3,1]=1
    grid3[5,1]=1
    grid3[6,1]=1
    grid3[7,1]=1
    grid3[8,1]=0
    grid3[1,2]=1
    grid3[2,2]=1
    grid3[3,2]=1
    grid3[5,2]=1
    grid3[1,3]=1
    grid3[5,3]=1
    grid3[7,3]=1
    grid3[8,3]=1
    grid3[1,4]=1
    grid3[2,4]=1
    grid3[3,4]=1
    grid3[5,4]=1
    grid3[7,4]=1
    grid3[3,5]=1
    grid3[5,5]=1
    grid3[6,5]=1
    grid3[7,5]=1
    grid3[1,6]=1
    grid3[3,6]=1
    grid3[4,6]=1
    grid3[5,6]=1
    grid3[1,7]=1
    grid3[7,7]=1
    grid3[8,7]=1
    grid3[1,8]=1
    grid3[3,8]=1
    grid3[4,8]=1
    grid3[5,8]=1
    grid3[6,8]=1
    grid3[7,8]=1
    grid3[0,9]=1
    grid3[1,9]=1
    grid3[3,9]=1
    grid3[5,9]=1
    grid3[1,10]=1
    grid3[3,10]=1
    grid3[7,10]=1
    grid3[1,11]=1
    grid3[2,11]=1
    grid3[3,11]=1
    grid3[4,11]=1
    grid3[5,11]=1
    grid3[6,11]=1
    grid3[7,11]=1
    
    print("Maze3 is: \n" + str(grid3))
    solver3=MazeSolver(grid3)
 
    is_connected3=solver3.is_connected(grid3,3,3,4,9)
    
    print("Coordinates 3,3 and 4,9 are connected: " + str(is_connected3))
    assert(is_connected3==False)

    '''
    Remove a part of the path blocking A and B to test reacheable (should now be true)
    '''
    grid3[8,7]=0
    print("Maze3 is: \n" + str(grid3))
    solver4=MazeSolver(grid3)
 
    is_connected4=solver4.is_connected(grid3,3,3,4,9)
    
    print("Coordinates 3,3 and 4,9 are connected: " + str(is_connected4))
    assert(is_connected4==True)
    
if __name__ == '__main__':
    main()   
     
