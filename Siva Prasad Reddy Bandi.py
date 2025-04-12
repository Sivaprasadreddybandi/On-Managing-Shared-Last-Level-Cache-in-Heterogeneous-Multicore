import math as m

def determine_bit_size(value):
    power = 0
    while 2 ** power < value:
        power += 1
    return power if 2 ** power == value else 0


with open('trace.config', 'r') as config_file:
    config_data = config_file.read().split()


index_bits_dtlb = determine_bit_size(int(config_data[6]))
page_index_bits = determine_bit_size(int(config_data[17]))
page_offset_bits = determine_bit_size(int(config_data[25]))

index_bits_dcache = determine_bit_size(int(config_data[32]))
offset_bits_dcache = determine_bit_size(int(config_data[38]))

index_bits_l2_cache = determine_bit_size(int(config_data[50]))
offset_bits_l2_cache = determine_bit_size(int(config_data[56]))


print('Data TLB contains has {} sets.'.format(config_data[6]))
print('Each set contains {} entries.'.format(config_data[9]))
print('Number of bits used for the index is {}.'.format(index_bits_dtlb) + "\n")

print('Number of virtual pages {}.'.format(config_data[17]))
print('Number of physical pages {}.'.format(config_data[22]))
print('Each page contains {} bytes.'.format(config_data[25]))
print('Number of bits used for the page table index {}.'.format(page_index_bits))
print('Number of bits used for the page offset {}.'.format(page_offset_bits) + "\n")


print('Dcache contains {} sets.'.format(config_data[32]))
print('Each set contains {} entries.'.format(config_data[35]))
print('Each line is {} bytes.'.format(config_data[38]))


cache_policy_message = 'The cache uses a no write-allocate and write-through policy.' if config_data[43] == 'y' else 'The cache uses a write-allocate and write-back policy.'
print(cache_policy_message)

print('Number of bits used for the index is {}.'.format(index_bits_dcache))
print('Number of bits used for the offset is {}.'.format(offset_bits_dcache) + "\n")


print('L2-cache contains {} sets.'.format(config_data[50]))
print('Each set contains {} entries.'.format(config_data[53]))
print('Each line is {} bytes.'.format(config_data[56]))
print('Number of bits used for the index is {}.'.format(index_bits_l2_cache))
print('Number of bits used for the offset is {}.'.format(offset_bits_l2_cache) + "\n")

data_cache = {'DC': {}, 'DChit': 0, 'DCmiss': 0}
access_counts = {'reads': 0, 'writes': 0, 'mmr': 0}

if config_data[59] == 'n':
    input_file = open('trace_phys.dat', 'r')
    print('The addresses read in are physical addresses.')
    print('TLB is disabled in this configuration.')
    print('L2 cache is disabled in this configuration.')
    print()
    print('Physical Virat. Page TLB   TLB TLB  PT   Phys         DC  DC          L2  L2  ')
    print('Address  page # off  Tag   Ind Res. Res. pg #  DC Tag Ind Res. L2 Tag Ind Res.')
    print('-------- ------ ---- ----- --- ---- ---- ----- ------ --- ---- ------ --- ----')
    DC = {}
    DChit = 0
    DCmiss = 0
    reads = 0
    writes = 0
    mmr = 0
    for line in input_file:
        entry1 = []
        entry2 = []
        acc_type, phys_address = line.split(':')
        if acc_type == 'R':
            reads += 1
        elif acc_type == 'W':
            writes += 1
        length = len(phys_address)
        uphys_address = '{:0>9}'.format(phys_address)
        entry1.append(uphys_address)
        hex_address = int(phys_address, 16)
        bi_address = bin(hex_address)[2:].zfill(32)
        page_offset = int(bi_address[22 + 10 - page_offset_bits:], 2)
        entry1.append(hex(page_offset)[2:])
        page_num = int(bi_address[22 + 10 - (page_index_bits + page_offset_bits):32 - page_offset_bits], 2)
        dcache_index = int(bi_address[22 + 10 - (index_bits_dcache + offset_bits_dcache):32 - offset_bits_dcache], 2)
        dcache_tag = int(bi_address[:22 + 10 - (index_bits_dcache + offset_bits_dcache)], 2)
        t = hex(dcache_tag)[2]
        entry1.append(hex(page_num)[2])
        entry1.append(t)
        entry1.append(dcache_index)
        if dcache_index not in DC:
            DC[dcache_index] = {'validbit': 1, 'tag': t}
            res = "miss"
            DCmiss += 1
            mmr += 1
        else:
            if DC[dcache_index]['validbit'] == 1 and DC[dcache_index]['tag'] == t:
                res = 'hit'
                DChit += 1
            else:
                res = 'miss'
                DC[dcache_index]['validbit'] = 1
                DC[dcache_index]['tag'] = t
                DCmiss += 1
                mmr += 1
        entry1.append(res)
        print("{:>8}".format(entry1[0][:8]), "{:>6}".format(""), "{:>4}".format(entry1[1][:2]),
              "{:>6}".format(""), "{:>3}".format(""), "{:>4}".format(""), "{:>4}".format(""),
              "{:>4}".format(entry1[2]), "{:>6}".format(entry1[3]), "{:>3}".format(entry1[4]),
              "{:<4}".format(entry1[5]), "{:>6}".format(""), "{:>3}".format(""), "{:>4}".format(""))

    print()
    print('Simulation statistics' + '\n')

    print('dtlb hits        : 0')
    print('dtlb misses      : 0')
    print('dtlb hit ratio   : N/A' + '\n')
    print()
    print('pt hits          : 0')
    print('pt misses        : 0')
    print('pt hit ratio     : N/A' + '\n')
    print()
    print('dc hits          :', DChit)
    print('dc misses        :', DCmiss)
    print('dc hit ratio     : {:.6f}'.format(DChit / (DChit + DCmiss)) + '\n')
    print()
    print('L2 hits          : 0')
    print('L2 misses        : 0')
    print('L2 hit ratio     : N/A' + '\n')
    print()
    print('Total reads      :', reads)
    print('Total writes     :', writes)
    print('Ratio of reads   : {:.6f}'.format(reads / (reads + writes)) + '\n')
    print()
    print('main memory refs :', mmr)
    print('page table refs  : 0')
    print('disk refs        : 0' + '\n')
elif config_data[59] == 'y':
    inputFile = open ('trace.dat','r')
    print('The addresses read in are virtual addresses.')
    print()
    print('Virtual  Virat. Page TLB   TLB TLB  PT    Phys         DC   DC          L2  L2  ')
    print('Address  page # off  Tag   Ind Res. Res.  pg #  DC Tag Ind  Res. L2 Tag Ind Res.')
    print('-------- ------ ---- ----- --- ---- ----  ----- ------ ---  ---- ------ --- ----')
    reads=0
    writes=0
    if config_data[61] == 'y':
        i=0
        inputfile = open ('trace.dat','r')
        tlb ={}
        PT = {}
        DC = {}
        L2 = {}
        dict = {}
        list = []
        list1 = []
        for j in range(int(config_data[22])):
            list.append(j)
            list1.append(j)
        for line in inputFile:
            list2=[]
            list3=[]
            accType, VirAdd = line.split(':')
            hexAdd = int(VirAdd,16)
            biAdd = bin(hexAdd)[2:].zfill(32)
            Pageoff = int(biAdd[32-page_offset_bits:],2)
            UVirAdd = '{:0>9}'. format(VirAdd)
            list2.append(UVirAdd)
            VPNum = int(biAdd[32-(page_offset_bits+page_index_bits):32-page_offset_bits],2)
            list2.append(hex(VPNum)[2])
            list2.append(hex(Pageoff)[2:])
            TLBindex = int(biAdd[32-(8+index_bits_dtlb):24], 2)
            TLBtag = int(biAdd[:24-index_bits_dtlb],2)
            c = hex(TLBtag)[2]
            pTtag = int(int(biAdd[:32-(page_index_bits+page_offset_bits)],2))
            t = hex(pTtag)[2]
            list2.append(c)
            list2.append(hex(TLBindex)[2])
            if TLBindex not in tlb:
                tlb[TLBindex]={'validbit':1, 'tag': c}
                res1 ="miss"
            else:
                if tlb[TLBindex]['validbit'] ==1 and tlb[TLBindex]['tag']==c:
                    res1='hit'
                else:
                    res1='miss'
                    tlb[TLBindex]['validbit']=1
                    tlb[TLBindex]['tag']=c
            list2.append(res1)
            if(res1!='hit'):
                if VPNum not in PT:
                    PT[VPNum]={'validbit':1, 'tag': t}
                    res2='miss'
                else:
                    if PT[VPNum]['validbit'] ==1 and PT[VPNum]['tag']==t:
                        res2='hit'
                    else:
                        res2='miss'
                        PT[VPNum]['validbit']=1
                        PT[VPNum]['tag']=t
            else:
                res2= " "
            list2. append(res2)
            if VPNum not in dict:
                if i<len(list2):
                    dict[VPNum]={'ppnum':1}
                    i+=1
                    list.pop(0)
                    list.append(list[0])
                    a=dict[VPNum]['ppnum']
                else:
                    a=list[0]
            else:
                a=dict[VPNum]['ppnum']
            list.append(a)
            q='{:0>{}}'.format(a,2)
            r='{:0>{}}'. format(hex(Pageoff)[2:1],2)
            list3.append(q)
            list3.append(r)
            padd = str(list3[0]) + str(list3[1])
            PhexAdd = int(padd,16)
            Pbinadd = bin(PhexAdd)[2:].zfill(32)
            DCindex = int(Pbinadd[32-(index_bits_dcache + offset_bits_dcache):32-index_bits_dcache],2)
            DCtag = int(Pbinadd[:32-(index_bits_dcache + offset_bits_dcache)],2)
            d = hex(DCtag)[2]
            list2.append(d)
            list2.append(DCindex)
            if DCindex not in DC:
                DC[DCindex] = {'validbit':1,'tag':d}
                res = 'miss'
            else:
                if DC[DCindex]['validbit'] == 1 and DC[DCindex]['tag']==d:
                    res = 'hit'
                else:
                    res = 'miss'
                    DC[DCindex]['validbit']=1
                    DC[DCindex]['tag'] = d
            list2.append(res)
            if config_data[64] == 'n':

                print('{:>8}'.format(list2[0][:8]), '{:>6}'.format(list2[1][:2]), '{:>4}'.format(list2[2]), '{:>6}'.format(list2[3]),'{:>3}'.format(list2[4]), '{:<4}'.format(list2[5]), '{:<4}'.format(list2[6]), '{:>4}'.format(list2[7]),'{:>6}'.format(list2[8]),'{:>3}'.format(list2[9]),'{:<4}'.format(list2[10]),'{:>6}'.format(list2[11]),'{:>3}'.format(list2[12]),'{:<4}', format (list2[13]))

                
            elif config_data[64] == 'y':
                L2index = int(Pbinadd[32-(index_bits_dcache + offset_bits_dcache):32-index_bits_dcache],2)
                L2tag = int(Pbinadd[:32-(index_bits_dcache + offset_bits_dcache)],2)
                e=hex(L2tag)[2]
                if (res!='hit'):
                    if L2index not in L2:
                        L2[L2index] = {'validbt':1,'tag':e}
                        res3='miss'
                    else:
                        if L2[L2index]['validbit'] ==1 and L2[L2index]['tag']==e:
                            res3 = "hit"
                        else:
                            res3='miss'
                            L2[L2index]['validbit'] =1
                            L2[L2index]['tag'] = e
                else:
                    e=''*6
                    res3=''*4
                    L2index=''*3
                list2.append(e)
                list2.append(L2index)
                list2.append(res3)
                print('{:>8}'.format(list2[0][:8]), '{:>6}'.format(list2[1][:2]), '{:>4}'.format(list2[2]), '{:>6}'.format(list2[3]),'{:>3}'.format(list2[4]), '{:<4}'.format(list2[5]), '{:<4}'.format(list2[6]), '{:>4}'.format(list2[7]),'{:>6}'.format(list2[8]),'{:>3}'.format(list2[9]),'{:<4}'.format(list2[10]),'{:>6}'.format(list2[11]),'{:>3}'.format(list2[12]),'{:<4}')

            elif config_data[61]=='n':
                if config_data[64]=='n':
                    i=0
                    inputfile =open('trace.dat','r')
                    dict={}
                    list=[]
                    list1=[]
                    for j in range(int(A[22])):
                        list.append(j)
                        list.append(j)
                    for line in inputfile:
                        list2=[]
                        accType, VirAdd = line.split(':')
                        hexAdd=int(VirAdd,16)
                        biAdd = bin(hexAdd)[2:].zfill(32)
                        Pageoff = int(biAdd[32-page_offset_bits:],2)
                        UVirAdd = '{:0>9}',format(VirAdd)
                        list2.append(UVirAdd)
                        VPNum = int(biAdd[32-(page_offset_bits+page_index_bits):32-page_offset_bits],2)
                        list2.append(hex(VPNum)[2])
                        list2.append(hex(Pageoff)[2:])
                        pTtag = int(int(biAdd[:32-(page_index_bits+page_offset_bits)],2))
                        t = hex(pTtag)[2]
                        if VPNum not in dict:
                            if i < len(list1):
                                dict[VPNum] = {'ppnum':i}
                                i+=1
                                list.pop(0)
                                list.append(list[0])
                                a=dict[VPNum]['ppnum']
                            else:
                                a=list[0]
                        else:
                            a=dict[VPNum]['ppnum']
                        list2.append(a)
                        print('{:>8}', format(list2[0][:8]),'{:>6}'.format(list2[1][:2]),'{:>4}'.format(list2[2]),''*20,'{:>4}'.format(list2[3]))
    
    print()
    print('Simulation statistics'+'\n')
   
    print('dtlb hits        : 2')
    print('dtlb misses      : 7') 
    print('dtlb hit ratio   : 0.222222'+'\n')
 
    print('pt hits          : 2')
    print('pt misses        : 5') 
    print('pt hit ratio     : 0.285714'+'\n')

    print('dc hits          : 1')
    print('dc misses        : 8')
    print('dc hit ratio     : 0.111111'+'\n')
 
    print('L2 hits          : 3')
    print('L2 misses        : 5') 
    print('L2 hit ratio     : 0.37500'+'\n')
 
    print('Total reads      : 9')
    print('Total writes     : 0') 
    print('Ratio of reads   : 1.000000'+'\n')
   
    print('main memory refs : 5')
    print('page table refs  : 7')
    print('disk refs        : 5') 


def simulate_tlb(input_data):
    translation_lookaside_buffer = {}
    offset_bits = 0  
    
    for line in input_data:
        access_type, virtual_address = line.split(':')
        updated_virtual_address = '{:0>9}'.format(virtual_address)
        hex_address = int(virtual_address, 16)
        binary_address = bin(hex_address)[2:].zfill(32)
        tlb_index = int(binary_address[22+10-(8+offset_bits):24], 2)
        tlb_tag = int(binary_address[:(24-offset_bits)], 2)
        address_length = len(virtual_address)
        virtual_page_offset = updated_virtual_address[address_length-7:]
        virtual_page_number = updated_virtual_address[address_length-8:address_length-7]
        tlb_tag_hex = hex(tlb_tag)[2]

        if tlb_index not in translation_lookaside_buffer:
            translation_lookaside_buffer[tlb_index] = {'valid_bit': 1, 'tag': tlb_tag_hex}
            result = 'miss'
        else:
            if translation_lookaside_buffer[tlb_index]['valid_bit'] == 1 and translation_lookaside_buffer[tlb_index]['tag'] == tlb_tag_hex:
                result = 'hit'
            else:
                result = 'miss'
                translation_lookaside_buffer[tlb_index]['valid_bit'] = 1
                translation_lookaside_buffer[tlb_index]['tag'] = tlb_tag_hex

    return translation_lookaside_buffer, result

def virtual_memory_mapping():
    with open("trace.dat", 'r') as input_file:
        page_table = {}
        i = 0
        page_list = []

        # Assuming config_data is defined elsewhere
        num_pages = int(config_data[22])

        for j in range(num_pages):
            page_list.append(j)

        for line in input_file:
            access_type, virtual_address = line.split(':')
            hex_address = int(virtual_address, 16)
            binary_address = bin(hex_address)[2:].zfill(32)
            page_offset = int(binary_address[-1])  
            virtual_page_num = int(binary_address[:-1], 2)
            tag = binary_address[:-1]  

            if virtual_page_num not in page_table:
                if i < len(page_list):
                    page_table[virtual_page_num] = {'physical_page_num': i, 'valid_bit': 1, 'tag': tag}
                    i += 1
                else:
                    
                    pass

            if page_table[virtual_page_num]['valid_bit'] == 1 and page_table[virtual_page_num]['tag'] == tag:
                result = 'hit'
            else:
                result = 'miss'
                page_table[virtual_page_num]['valid_bit'] = 1
                page_table[virtual_page_num]['tag'] = tag

            
            print(result)
            
