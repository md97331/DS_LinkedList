class LinkedList:
    class Node:
        def __init__(self, val, prior=None, next=None):
            self.val = val
            self.prior = prior
            self.next  = next
    
    def __init__(self):
        self.head = LinkedList.Node(None) # sentinel node (never to be removed)
        self.head.prior = self.head.next = self.head # set up "circular" topology
        self.length = 0
        
        
    ### prepend and append, below, from class discussion
        
    def prepend(self, value):
        n = LinkedList.Node(value, prior=self.head, next=self.head.next)
        self.head.next.prior = self.head.next = n
        self.length += 1
        
    def append(self, value):
        n = LinkedList.Node(value, prior=self.head.prior, next=self.head)
        n.prior.next = n.next.prior = n
        self.length += 1
            
            
    ### subscript-based access ###
    
    def _normalize_idx(self, idx):
        nidx = idx
        if nidx < 0:
            nidx += len(self)
            if nidx < 0:
                nidx = 0
        return nidx
    
    def __getitem__(self, idx):
        """Implements `x = self[idx]`"""
        assert(isinstance(idx, int))
        nidx = self._normalize_idx(idx)
        if nidx >= self.length:
            raise IndexError
        else:
            #start at head, skip the NONE sentinel, now at index 0, while loop to walk to nidx, return data
            # or figure out closer to head or head.prior(tail), make the walk shorter
            if idx< (self.length/2):    #start at head.next, walk forward idx number of nodes
                current=self.head.next
                count=0
                while count<nidx:
                    current=current.next
                    count+=1
            else:    #start at head.prior, walk backward len(self.data)-idx-1 number of nodes
                current=self.head.prior
                count=self.length-1
                while count>nidx:
                    current=current.prior
                    count-=1
            return current.val
                
    def __setitem__(self, idx, value):
        """Implements `self[idx] = x`"""
        assert(isinstance(idx, int))
        nidx = self._normalize_idx(idx)
        if nidx >= self.length:
            raise IndexError
        else:
            #start at head, skip the NONE sentinel, now at index 0, while loop to walk to nidx, update data
            # or figure out closer to head or head.prior(tail), make the walk shorter
            if idx< (self.length/2):    #start at head.next, walk forward idx number of nodes
                current=self.head.next
                count=0
                while count<nidx:
                    current=current.next
                    count+=1
            else:    #start at head.prior, walk backward len(self.data)-idx-1 number of nodes
                current=self.head.prior
                count=self.length-1
                while count>nidx:
                    current=current.prior
                    count-=1
            current.val=value

    def __delitem__(self, idx):
        """Implements `del self[idx]`"""
        assert(isinstance(idx, int))
        nidx = self._normalize_idx(idx)
        if nidx >= self.length:
            raise IndexError
        else:
            #start at head, skip the NONE sentinel, now at index 0, while loop to walk to nidx, splice out the node
            # or figure out closer to head or head.prior(tail), make the walk shorter
            if idx< (self.length/2):    #start at head.next, walk forward idx number of nodes
                current=self.head.next
                count=0
                while count<nidx:
                    current=current.next
                    count+=1
            else:    #start at head.prior, walk backward len(self.data)-idx-1 number of nodes
                current=self.head.prior
                count=self.length-1
                while count>nidx:
                    current=current.prior
                    count-=1
            current.prior.next = current.next
            current.next.prior = current.prior
            self.length-=1
    

    ### stringification ###
    
    def __str__(self):
        """Implements `str(self)`. Returns '[]' if the list is empty, else
        returns `str(x)` for all values `x` in this list, separated by commas
        and enclosed by square brackets. E.g., for a list containing values
        1, 2 and 3, returns '[1, 2, 3]'."""

        strs = '['
        cur = self.head.next
        for _ in range(self.length):
            strs += f'{str(cur.val)}, '
            cur = cur.next
        strs = strs.strip(', ')
        strs += ']'
        return strs
        
    def __repr__(self):
        """Supports REPL inspection. (Same behavior as `str`.)"""
        return str(self)


    ### single-element manipulation ###
        
    def insert(self, idx, value):
        """Inserts value at position idx, shifting the original elements down the
        list, as needed. Note that inserting a value at len(self) --- equivalent
        to appending the value --- is permitted. Raises IndexError if idx is invalid."""
        nidx = self._normalize_idx(idx)
        if nidx > self.length:
            raise IndexError()

        curr = self.head.next
        for i in range(nidx):
            curr = curr.next

        n = LinkedList.Node(value, prior = curr.prior, next = curr)
        curr.prior.next = curr.prior = n

        self.length +=1
    
    def pop(self, idx=-1):
        """Deletes and returns the element at idx (which is the last element,
        by default)."""

        nidx = self._normalize_idx(idx)
        if nidx >= self.length or self.length == 0:
            raise IndexError 

        rtn = self[nidx]
        del self[nidx]
        return rtn
    
    def remove(self, value):
        """Removes the first (closest to the front) instance of value from the
        list. Raises a ValueError if value is not found in the list."""
        curr = self.head.next
        for i in range(self.length):
            if curr.val == value:
                self.pop(i)
                return i
            curr = curr.next
        raise ValueError()
    

    ### predicates (T/F queries) ###
    
    def __eq__(self, other):
        """Returns True if this LinkedList contains the same elements (in order) as
        other. If other is not an LinkedList, returns False."""
        assert(isinstance(other, LinkedList))
        if self.length != other.length:
            return False
        iSelf = iter(self)
        iOther = iter(other)

        for i in zip(iSelf, iOther):
            if i[0] != i[1]:
                return False
        return True

    def __contains__(self, value):
        """Implements `val in self`. Returns true if value is found in this list."""
        for item in iter(self):
            if item == value:
                return True
        return False


    ### queries ###
    
    def __len__(self):
        """Implements `len(self)`"""
        return self.length
    
    def min(self):
        """Returns the minimum value in this list."""
        min = self.head.next.val
        curr = self.head.next
        for i in range(self.length):
            if min>curr.val:
                min=curr.val
            curr = curr.next
        return min
    
    def max(self):
        """Returns the maximum value in this list."""
        max = self.head.next.val
        curr = self.head.next
        for i in range(self.length):
            if max<curr.val:
                max=curr.val
            curr = curr.next
        return max
    
    def index(self, value, i=0, j=None):
        """Returns the index of the first instance of value encountered in
        this list between index i (inclusive) and j (exclusive). If j is not
        specified, search through the end of the list for value. If value
        is not in the list, raise a ValueError."""

        i_nidx = self._normalize_idx(i)
        if j==None:
            j= self.length
        j_nidx = self._normalize_idx(j)

        curr = self.head.next
        for _ in range(i_nidx):
            curr= curr.next
        for idx in range(i_nidx, j_nidx):
            if value == curr.val:
                return idx
            curr = curr.next
        raise ValueError()
    
    def count(self, value):
        """Returns the number of times value appears in this list."""
        count=0
        for val in iter(self):
            if val == value:
                count+=1
        return count

    
    ### bulk operations ###

    def __add__(self, other):
        """Implements `self + other_list`. Returns a new LinkedList
        instance that contains the values in this list followed by those 
        of other."""
        assert(isinstance(other, LinkedList))
        nLinklst = LinkedList()

        curr = self.head.next
        for _ in range(self.length):
            nLinklst.append(curr.val)
            curr = curr.next
        curr2 = other.head.next
        for _ in range (other.length):
            nLinklst.append(curr2.val)
            curr2 = curr2.next
        return nLinklst        
    
    def clear(self):
        """Removes all elements from this list."""
        self.head.next = self.head.prior = self.head
        self.length = 0
        
    def copy(self):
        """Returns a new LinkedList instance (with separate Nodes), that
        contains the same values as this list."""
        nLinklst= LinkedList()
        for x in self:
            nLinklst.append(x)
        return nLinklst     

    def extend(self, other):
        """Adds all elements, in order, from other --- an Iterable --- to this list."""
        for val in other:
            self.append(val)

            
    ### iteration ###

    def __iter__(self):
        """Supports iteration (via `iter(self)`)"""
        curr = self.head.next
        while curr is not self.head:
            yield curr.val
            curr = curr.next
