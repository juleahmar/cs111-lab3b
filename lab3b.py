# NAME: Karl Marrett,Jules Ahmar
# EMAIL: kdmarrett@gmail.com,juleahmar@g.ucla.edu
# ID: 705225374,205301445

import sys
import csv
import pdb

#keeps track of block references
class b_ref:
    def __init__(self, arg1, arg2, arg3, arg4):
        self.block_type = arg1
        self.block_num = arg2
        self.inode_num = arg3
        self.offset = arg4

#these classes were created based off of lab3a -> ext2_fs.h file
class superblock:
    def __init__(self, arg1, arg2, arg3, arg4, arg5): 
        self.blocks = arg1
        self.inodes = arg2
        self.block_size = arg3
        self.inode_size = arg4
        self.first_avail_inode = arg5

class inode:
    def __init__(self, arg1, arg2, arg3, arg4):
        self.num = arg1
        self.type = arg2
        self.links = arg3
        self.addr = arg4

class directory:
    def __init__(self, arg1, arg2, arg3, arg4):
        self.parent_inode = arg1
        self.offset = arg2
        self.inode_ref = arg3
        self.name = arg4

class indirect:
    def __init__(self, arg1, arg2, arg3, arg4):
        self.file = arg1
        self.level = arg2
        self.offset = arg3
        self.bref = arg4

class group:
    def __init__(self, arg1, arg2, arg3):
        self.bnum = arg1
        self.inum = arg2
        self.first_inode = arg3

#set to 1 if we need to exit(2)
wrong = 0

#lists
d_s = []
ino_s = []
idir_s = []
ifrees = []
bfrees = []
g_s = []

#sb = superblock(0,0,0,0,0,0,0)
blocks = 0
exist = {}

rb = set([0, 1, 2, 3, 4, 5, 6, 7, 64])

def all_checks():
    ################################
    #DUPLICATE CHECKING
    ################################   
    global wrong
    global sb
    for i in ino_s:
        addr = i.addr
        for b in range(len(addr)):
            node = addr[b]
            if not node:
                continue
            if node in bfrees:
                wrong = 1
                print('ALLOCATED BLOCK ' + str(node) + ' ON FREELIST')
            else:
                if node > sb.blocks or node < 0:
                    if b == 14:
                        print('INVALID TRIPLE INDIRECT BLOCK ' + str(node) + ' IN INODE ' + str(i.num) + ' AT OFFSET 65804')
                        wrong = 1
                    elif b == 13:
                        print('INVALID DOUBLE INDIRECT BLOCK ' + str(node) + ' IN INODE ' + str(i.num) + ' AT OFFSET 268')
                        wrong = 1
                    elif b == 12:
                        print('INVALID INDIRECT BLOCK ' + str(node) + ' IN INODE ' + str(i.num) + ' AT OFFSET 12')
                        wrong = 1
                    else:
                        print('INVALID BLOCK ' + str(node) + ' IN INODE ' + str(i.num) + ' AT OFFSET 0')
                        wrong = 1
                if node in rb:
                    if b == 14:
                        print('RESERVED TRIPLE INDIRECT BLOCK ' + str(node) + ' IN INODE ' + str(i.num) + ' AT OFFSET 65804')
                        wrong = 1
                    elif b == 13:
                        print('RESERVED DOUBLE INDIRECT BLOCK ' + str(node) +  ' IN INODE ' + str(i.num) + ' AT OFFSET 268')
                        wrong = 1
                    elif b == 12:
                        print('RESERVED INDIRECT BLOCK ' + str(node) + ' IN INODE ' + str(i.num) + ' AT OFFSET 12')
                        wrong = 1
                    else:
                        print('RESERVED BLOCK ' + str(node) + ' IN INODE ' + str(i.num) + ' AT OFFSET 0')
                        wrong = 1
                if node not in rb and node >= 0 and node <= sb.blocks:
                    if node not in exist:
                        if b == 14:
                            exist[node] = []
                            exist[node].append(b_ref("TRIPLE INDIRECT BLOCK", node, i.num, 65804))
                        elif b == 13:
                            exist[node] = []
                            exist[node].append(b_ref("DOUBLE INDIRECT BLOCK", node, i.num, 268))
                        elif b == 12:
                            exist[node] = []
                            exist[node].append(b_ref("INDIRECT BLOCK", node, i.num, 12))
                        else:
                            exist[node] = []
                            exist[node].append(b_ref("BLOCK", node, i.num, 0))
                    else:
                        if b == 14:
                            exist[node].append(b_ref("TRIPLE INDIRECT BLOCK", node, i.num, 65804))
                        elif b == 13:
                            exist[node].append(b_ref("DOUBLE INDIRECT BLOCK", node, i.num, 268))
                        elif b == 12:
                            exist[node].append(b_ref("INDIRECT BLOCK", node, i.num, 12))
                        else:
                            exist[node].append(b_ref("BLOCK", node, i.num, 0))

    for i in idir_s:
        if i.bref in bfrees:
            print("ALLOCATED BLOCK " + str(i.bref) + " ON FREELIST")
            wrong = 1
        else:
            if i.bref not in exist:
                if i.level == 3: 
                    exist[i.bref] = []
                    exist[i.bref].append(b_ref("TRIPLE INDIRECT BLOCK", i.bref, i.file, i.offset))
                elif i.level == 2:
                    exist[i.bref] = []
                    exist[i.bref].append(b_ref("DOUBLE INDIRECT BLOCK", i.bref, i.file, i.offset))
                elif i.level == 1:
                    exist[i.bref] = []
                    exist[i.bref].append(b_ref("INDIRECT BLOCK", i.bref, i.file, i.offset))
                else:
                    exist[i.bref] = []
                    exist[i.bref].append(b_ref("BLOCK", i.bref, i.file, i.offset))
            elif i.bref in exist:
                if i.level == 3: 
                    exist[i.bref].append(b_ref("TRIPLE INDIRECT BLOCK", i.bref, i.file, i.offset))
                elif i.level == 2:
                    exist[i.bref].append(b_ref("DOUBLE INDIRECT BLOCK", i.bref, i.file, i.offset))
                elif i.level == 1:
                    exist[i.bref].append(b_ref("INDIRECT BLOCK", i.bref, i.file, i.offset))
                else:
                    exist[i.bref].append(b_ref("BLOCK", i.bref, i.file, i.offset))
            if i.bref in rb:
                if i.level == 3: 
                    print("RESERVED TRIPLE INDIRECT BLOCK " + str(i.bref) + " IN INODE " + str(i.file) + " AT OFFSET " + str(i.offset))
                    wrong = 1
                elif i.level == 2:
                    print("RESERVED DOUBLE INDIRECT BLOCK " + str(i.bref) + " IN INODE " + str(i.file) + " AT OFFSET " + str(i.offset))
                    wrong = 1
                elif i.level == 1:
                    print("RESERVED INDIRECT BLOCK " + str(i.bref) + " IN INODE " + str(i.file) + " AT OFFSET " + str(i.offset))
                    wrong = 1
                else:
                    print("RESERVED BLOCK " + str(i.bref) + " IN INODE " + str(i.file) + " AT OFFSET " + str(i.offset))
                    wrong = 1
            if int(i.bref) > sb.blocks or int(i.bref) < 0:
                if i.level == 3: 
                    print("INVALID TRIPLE INDIRECT BLOCK " + str(i.bref) + " IN INODE " + str(i.file) + " AT OFFSET " + str(i.offset))
                    wrong = 1
                elif i.level == 2:
                    print("INVALID DOUBLE INDIRECT BLOCK " + str(i.bref) + " IN INODE " + str(i.file) + " AT OFFSET " + str(i.offset))
                    wrong = 1
                elif i.level == 1:
                    print("INVALID INDIRECT BLOCK " + str(i.bref) + " IN INODE " + str(i.file) + " AT OFFSET " + str(i.offset))
                    wrong = 1
                else:
                    print("INVALID BLOCK " + str(i.bref) + " IN INODE " + str(i.file) + " AT OFFSET " + str(i.offset))
                    wrong = 1

    ################################
    #DUPLICATE/UNREFERENCED CHECKING
    ################################
    start = int(sb.inode_size * g_s[0].inum/sb.block_size) + g_s[0].first_inode
    end = g_s[0].bnum
    for i in range(start, end):
        if i not in exist and i not in bfrees:
            print('UNREFERENCED BLOCK ' + str(i))
            wrong = 1
        if i in exist and len(exist[i]) >= 2:
            for j in exist[i]:
                print('DUPLICATE ' + str(j.block_type) +  ' ' + str(j.block_num) +  ' IN INODE ' + str(j.inode_num) + ' AT OFFSET ' + str(j.offset))
                wrong = 1
        
    #################################
    #INODE CHECK STUFF
    #################################
    for inode in ino_s:
        if inode.type in ('f', 'd', 's'):
            # should not be in the free list
            if inode.num in ifrees:
                print("ALLOCATED INODE %d ON FREELIST" % inode.num)
        else:
            # asserting because I'm not sure if this edge case needs
            # to be handled yet
            assert(inode.type is '0')
            if inode.num not in ifrees:
                print("UNALLOCATED INODE %d NOT ON FREELIST" % inode.num)

    
    #################################
    #DIRECTORY CHECK STUFF
    #################################
    # spec:
    # Every allocated I-node should be referred to by the number of directory
    # entries that is equal to the reference count recorded in the I-node. 

    # For any allocated I-node whose reference count does not match the number
    # of discovered links, an error message like the following should be
    # generated to stdout:

    ##INSERT DIRECTORY CHECKS HERE





def main():
    global sb
    try:
        f = open(sys.argv[1], "r")
    except:
        sys.stderr.write("Invalid argument.\n")
        sys.exit(1)
    
    data = f.readlines()

    for j in data:
        i = j.split(",")
        x = i[0]
        if x == 'SUPERBLOCK':
            sb = superblock(int(i[1]), int(i[2]), int(i[3]), int(i[4]), int(i[7]))
        elif x == 'INODE':
            l = list(map(int,i[12:]))
            ino = inode(int(i[1]), i[2], int(i[6]), l)
            ino_s.append(ino)
        elif x == 'DIRENT':
            d = directory(int(i[1]), int(i[2]), int(i[3]), i[6])
            d_s.append(d)
        elif x == 'INDIRECT':
            idir = indirect(int(i[1]), int(i[2]), int(i[3]), int(i[5]))
            idir_s.append(idir)
        elif x == 'BFREE':
            bfree = int(i[1])
            bfrees.append(bfree)
        elif x == 'IFREE':
            ifree = int(i[1])
            ifrees.append(ifree)
        elif x == 'GROUP':
            g = group(int(i[2]), int(i[3]), int(i[8]))
            g_s.append(g)
        else:
            sys.exit(1)

    all_checks()

    if not wrong:
        sys.exit(0)
    else:
        sys.exit(2)

if __name__ == "__main__":
    main()

