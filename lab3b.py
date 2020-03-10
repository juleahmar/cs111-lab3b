# NAME: Karl Marrett,Jules Ahmar
# EMAIL: kdmarrett@gmail.com,juleahmar@g.ucla.edu
# ID: 705225374,205301445

import sys
import csv

#set to 1 if we need to exit(2)
err_flag = 0

#lists
d_s = []
ino_s = []
idir_s = []
ifrees = []
bfrees = []
g_s = []

blocks = 0
exist = {}

rb = set([0, 1, 2, 3, 4, 5, 6, 7, 64])

def block_check():
    #do stuff
    for i in idir_s:
        

    for i in ino_s:
        for b in range(len(i.block_address)):
            node = i.block_address[b]
            if node in bfrees:
                err_flag = 1
                print('ALLOCATED BLOCK ' + str(node) + ' ON FREELIST')
            else:
                ofst = 0
                t = ""
                if node > blocks or node < 0:
                    if b == 14:
                        print('INVALID TRIPLE INDIRECT BLOCK IN INODE ' + str(node) + ' AT OFFSET 65804')
                        t = "TRIPLE INDIRECT BLOCK"
                        ofst = 65804
                        err_flag = 1
                    elif b == 13:
                        print('INVALID DOUBLE INDIRECT BLOCK IN INODE ' + str(node) + ' AT OFFSET 268')
                        t = "DOUBLE INDIRECT BLOCK"
                        ofst = 268
                        err_flag = 1
                    elif b == 12:
                        print('INVALID INDIRECT BLOCK IN INODE ' + str(node) + ' AT OFFSET 12')
                        t = "INDIRECT BLOCK"
                        ofst = 12
                        err_flag = 1
                if node in rb:
                    if b == 14:
                        print('RESERVED TRIPLE INDIRECT BLOCK IN INODE ' + str(node) + ' AT OFFSET 65804')
                        t = "TRIPLE INDIRECT BLOCK"
                        ofst = 65804
                        err_flag = 1
                    elif b == 13:
                        print('RESERVED DOUBLE INDIRECT BLOCK IN INODE ' + str(node) + ' AT OFFSET 268')
                        t = "DOUBLE INDIRECT BLOCK"
                        ofst = 268
                        err_flag = 1
                    elif b == 12:
                        print('RESERVED INDIRECT BLOCK IN INODE ' + str(node) + ' AT OFFSET 12')
                        t = "INDIRECT BLOCK"
                        ofst = 12
                        err_flag = 1
                if node not in rb and node >= 0 and node <= blocks and b not in exist:
                    exist[node] = []
                    exist[node].append(block(t, node, i.inode_number, ofst))
                else:
                    exist[node].append(block(t, node, i.inode_number, ofst))
                     


def inode_check():
    #do stuff

def dir_check():
    #do stuff

class superblock:
    def __init__(self, arg1, arg2, arg3, arg4, arg5, arg6, arg7): 
        self.total_num_blocks = arg1
        self.total_num_inode = arg2
        self.block_size = arg3
        self.inode_size = arg4
        self.block_per_group = arg5
        self.inode_per_group = arg6
        self.first_nonreserved_inode = arg7

class block:
    def __init__(self, arg1, arg2, arg3, arg4):
        self.block_type = arg1
        self.block_num = arg2
        self.inode_num = arg3
        self.offset = arg4

class inode:
    def __init__(self, arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, arg11, arg12):
        self.inode_number = arg1
        self.file_type = arg2
        self.mode = arg3
        self.owner = arg4
        self.group = arg5
        self.link_count = arg6
        self.ctime = arg7
        self.mtime = arg8
        self.atime = arg9
        self.file_size = arg10
        self.disk_space = arg11
        self.block_address = arg12

class directory:
    def __init__(self, arg1, arg2, arg3, arg4, arg5, arg6):
        self.parent_inode_number = arg1
        self.logical_offset = arg2
        self.reference_inode = arg3
        self.entry_length = arg4
        self.name_length = arg5
        self.name = arg6

class indirect:
    def __init__(self, arg1, arg2, arg3, arg4, arg5):
        self.owning_file = arg1
        self.level = arg2
        self.logical_offset = arg3
        self.blocknum_scanned = arg4
        self.blocknum_reference = arg5

class group:
    def __init__(self, arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8):
        self.group_number = arg1
        self.block_number_in_group = arg2
        self.inode_number_in_group = arg3 
        self.freeblock_number = arg4
        self.freeinode_number = arg5
        self.freeblock_bitmap_num = arg6
        self.freeinode_bitmap_num = arg7
        self.first_block_inode = arg8


def main():
    try:
        f = open(sys.argv[1], "r")
    except:
        sys.stderr.write("Invalid argument.\n")
        sys.exit(1)

    csv_read = csv.reader(f)

    for i in csv_read:
        x = i[0]

        if x == 'SUPERBLOCK':
            sb = superblock(int(i[1]), int(i[2]), int(i[3]), int(i[4]), int(i[5]), int(i[6]), int(i[7]))
        elif x == 'INODE':
            l = list(map(int,i[12:]))
            ino = inode(int(i[1]), int(i[2]), int(i[3]), int(i[4]), int(i[5]), int(i[6]), int(i[7]), int(i[8]), int(i[9]), int(i[10]), int(i[11]), l)
            ino_s.append(ino)
        elif x == 'DIRENT':
            d = directory(int(i[1]), int(i[2]), int(i[3]), int(i[4]), int(i[5]), int(i[6]))
            d_s.append(d)
        elif x == 'INDIRECT':
            idir = indirect(int(i[1]), int(i[2]), int(i[3]), int(i[4]), int(i[5]))
            idir_s.append(idir)
        elif x == 'BFREE':
            bfree = int(i[1])
            bfrees.append(bfree)
        elif x == 'IFREE':
            ifree = int(i[1])
            ifrees.append(ifree)
        elif x == 'GROUP':
            g = group(int(i[1]), int(i[2]), int(i[3]), int(i[4]), int(i[5]), int(i[6]), int(i[7]), int(i[8]))
            g_s.append(g)

    #block audits
    block_check()

    #inode audits
    inode_check()

    #directory audits
    dir_check()

    if not err_flag:
        sys.exit(0)
    else:
        sys.exit(2)

if __name__ == "__main__":
    main()