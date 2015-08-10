class Member(object):
    def __init__(self, founder):
        """ 
        founder: string
        Initializes a member. 
        Name is the string of name of this node,
        parent is None, and no children
        """        
        self.name = founder
        self.parent = None         
        self.children = []    

    def __str__(self):
        return self.name    

    def add_parent(self, mother):
        """
        mother: Member
        Sets the parent of this node to the `mother` Member node
        """
        self.parent = mother   

    def get_parent(self):
        """
        Returns the parent Member node of this Member
        """
        return self.parent 

    def is_parent(self, mother):
        """
        mother: Member
        Returns: Boolean, whether or not `mother` is the 
        parent of this Member
        """
        return self.parent == mother  

    def add_child(self, child):
        """
        child: Member
        Adds another child Member node to this Member
        """
        self.children.append(child)   

    def is_child(self, child):
        """
        child: Member
        Returns: Boolean, whether or not `child` is a
        child of this Member
        """
        return child in self.children 


class Family(object):
    def __init__(self, founder):
        """ 
        Initialize with string of name of oldest ancestor

        Keyword arguments:
        founder -- string of name of oldest ancestor
        """

        self.names_to_nodes = {}
        self.root = Member(founder)
        self.names_to_nodes[founder] = self.root
        self.visited = None
        self.clock = None
        self.pre_order = None
        self.post_order = None

    def set_children(self, mother, list_of_children):
        """
        Set all children of the mother. 

        Keyword arguments: 
        mother -- mother's name as a string
        list_of_children -- children names as strings
        """
        # convert name to Member node (should check for validity)
        mom_node = self.names_to_nodes[mother]   
        # add each child
        for c in list_of_children:           
            # create Member node for a child   
            c_member = Member(c)               
            # remember its name to node mapping
            self.names_to_nodes[c] = c_member    
            # set child's parent
            c_member.add_parent(mom_node)
            # set the parent's child
            mom_node.add_child(c_member)

    def run_dfs(self):
        self.visited = []
        self.clock = 1
        self.pre_order = {}
        self.post_order = {}
        self.depth_first_search(self.root)

    def depth_first_search(self, node):
        self.visited.append(node)
        self.pre_visit(node)
        for child in node.children:
            if child.name not in self.visited:
                self.depth_first_search(child)
        self.post_visit(node)

    def pre_visit(self, node):
        self.pre_order[node.name] = self.clock
        self.clock += 1

    def post_visit(self, node):
        self.post_order[node.name] = self.clock
        self.clock += 1

    def cousin(self, a, b):
        """
        Returns a tuple of (the cousin type, degree removed) 

        Keyword arguments: 
        a -- string that is the name of node a
        b -- string that is the name of node b

        cousin type:
          -1 if a and b are the same node.
          -1 if either one is a direct descendant of the other
          >=0 otherwise, it calculates the distance from 
          each node to the common ancestor.  Then cousin type is 
          set to the smaller of the two distances, as described 
          in the exercises above

        degrees removed:
          >= 0
          The absolute value of the difference between the 
          distance from each node to their common ancestor.
        """
        
        ## YOUR CODE HERE ####
        self.run_dfs()
        cousin = -1
        degree = 0
        if self.pre_order[a] == self.pre_order[b]:           # same person
            pass
        elif (    self.pre_order[a]  > self.pre_order[b]
              and self.post_order[a] < self.post_order[b]):  # a is descendant of b
            degree = self.distance_to_ancestor(a, b)
        elif (    self.pre_order[a]  < self.pre_order[b]
              and self.post_order[a] > self.post_order[b]):  # b is descendant of a
            degree = self.distance_to_ancestor(b, a)
        else:                                                # a and b have common ancestor
            cousin, degree = self.get_cousin_and_degree(a, b)
        return cousin, degree

    def distance_to_ancestor(self, descendant_name, ancestor_name, distance=0):
        descendant = self.names_to_nodes[descendant_name]
        ancestor = self.names_to_nodes[ancestor_name]
        if descendant == ancestor:
            return distance
        else:
            return self.distance_to_ancestor(descendant.parent.name, ancestor_name, distance + 1)

    def get_cousin_and_degree(self, person_1_name, person_2_name):
        generation_1 = self.distance_to_ancestor(person_1_name, self.root.name)
        generation_2 = self.distance_to_ancestor(person_2_name, self.root.name)
        degree = abs(generation_1 - generation_2)
        if generation_1 > generation_2:
            person_1 = self.get_nth_parent(person_1_name, degree)
            person_2 = self.names_to_nodes[person_2_name]
        elif generation_2 > generation_1:
            person_1 = self.names_to_nodes[person_1_name]
            person_2 = self.get_nth_parent(person_2_name, degree)
        else:
            person_1 = self.names_to_nodes[person_1_name]
            person_2 = self.names_to_nodes[person_2_name]
        cousin = self.distance_to_common_ancestor(person_1, person_2)
        return cousin, degree

    def distance_to_common_ancestor(self, person_1, person_2, distance=0):
        if person_1.parent == person_2.parent:
            return distance
        else:
            return self.distance_to_common_ancestor(person_1.parent, person_2.parent, distance + 1)

    def get_nth_parent(self, person_name, n):
        person = self.names_to_nodes[person_name]
        if n == 0:
            return person
        else:
            return self.get_nth_parent(person.parent.name, n - 1)

f = Family("a")
f.set_children("a", ["b", "c"])
f.set_children("b", ["d", "e"])
f.set_children("c", ["f", "g"])

f.set_children("d", ["h", "i"])
f.set_children("e", ["j", "k"])
f.set_children("f", ["l", "m"])
f.set_children("g", ["n", "o", "p", "q"])

words = ["zeroth", "first", "second", "third", "fourth", "fifth", "non"]

## These are your test cases. 

## The first test case should print out:
## 'b' is a zeroth cousin 0 removed from 'c'
t, r = f.cousin("b", "c")
print "'b' is a", words[t],"cousin", r, "removed from 'c'"

## For the remaining test cases, use the graph to figure out what should 
## be printed, and make sure that your code prints out the appropriate values.

t, r = f.cousin("d", "f")
print "'d' is a", words[t],"cousin", r, "removed from 'f'"

t, r = f.cousin("i", "n")
print "'i' is a", words[t],"cousin", r, "removed from 'n'"

t, r = f.cousin("q", "e")
print "'q' is a", words[t], "cousin", r, "removed from 'e'"

t, r = f.cousin("h", "c")
print "'h' is a", words[t], "cousin", r, "removed from 'c'"

t, r = f.cousin("h", "a")
print "'h' is a", words[t], "cousin", r, "removed from 'a'"

t, r = f.cousin("h", "h")
print "'h' is a", words[t], "cousin", r, "removed from 'h'"

t, r = f.cousin("a", "a")
print "'a' is a", words[t], "cousin", r, "removed from 'a'"
