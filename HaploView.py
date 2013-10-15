#!/opt/Python/2.7.3/bin/python
import sys
from collections import defaultdict
import re
import os
import argparse
from numpy import *

def usage():
    test="name"
    message='''
Draw for each 5 Mb window on chromosome:
python HaploView.py --input ../input/BGI.SNP.Jap.matrix.1 --window --output BGI_Jap
or draw a big view of whole chromosome using 2% of SNPs random by RandomLine.py:
python HaploView.py --input ../input/BGI.SNP.Jap.matrix.4 --output BGI_Jap_chr

Genotype data are input as matrix:
chromosome01 411 A A A A A A A A A A A A A A A A A A A G A A A
chromosome01 465 G G G G G G G G G G G G G G G G G G G A G G G
chromosome01 482 T T T T T T T T T T T T T T T T T T T C T T T

    '''
    print message

def matrix2haploview(matrix,output):
    chro    = ''
    data    = defaultdict(lambda: defaultdict(list))
    marker  = defaultdict(list)
    s       = re.compile(r'(\d+)')
    if not os.path.isdir(output):
        os.system('mkdir ' + output)
    with open (matrix, 'r') as matrixfh:
        for line in matrixfh:
            line = line.rstrip()
            samplen = 0
            unit    = re.split(r'\s+',line)
            m       = s.search(unit[0])
            chrn    = m.groups(0)[0]
            chro    = 'Chr' + str(chrn)
            marker[chro].append(unit[1])
            #print unit[1], index
            for geno in unit[2:]:
                samplen += 1
                data[chro][samplen].append(geno)
    for chro in sorted(data.keys()):
        pedigree = 0
        ofile = output + '/' + chro + '.ped'
        with open (ofile, 'w') as ofilehd:    
            for samplen in sorted(data[chro].keys()):
                haplotype = []
                pedigree  += 1
                strain    = output + str(samplen)
                haplotype.append(str(pedigree))
                haplotype.append(strain)
                haplotype.extend(['0','0','2','0'])
                for g in data[chro][samplen]:
                    haplotype.append(g + " " + g)              
                genotype = "\t".join(haplotype)
                print >> ofilehd, genotype
        mfile = output + '/' + chro + '.inf'
        with open (mfile, 'w') as mfilehd:
            for pos in marker[chro]:
                markern = 'm' + str("%08d" %int(pos))
                print >> mfilehd, markern + '\t' + pos
        prefix  = output + '/' + chro
        cmdline = 'java -jar Haploview.jar -nogui -memory 5000 -pedfile ' + ofile + ' -info ' + mfile + ' -out ' + prefix + ' -compressedpng -dprime -maxdistance 50000'
        os.system(cmdline) 
    
def matrix2haploview_win(matrix,output):
    chro    = ''
    win     = 5000000
    data    = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    marker  = defaultdict(lambda: defaultdict(list))
    s       = re.compile(r'(\d+)')
    if not os.path.isdir(output):
        os.system('mkdir ' + output)
    with open (matrix, 'r') as matrixfh:
        for line in matrixfh:
            line = line.rstrip()
            samplen = 0
            unit    = re.split(r'\s+',line)
            index   = int(unit[1])/int(win)
            m       = s.search(unit[0])
            chrn    = m.groups(0)[0]
            chro    = 'Chr' + str(chrn)
            marker[chro][index].append(unit[1])
            #print unit[1], index
            for geno in unit[2:]:
                samplen += 1
                data[chro][index][samplen].append(geno)
    for chro in sorted(data.keys()):
        for tag in sorted(data[chro].keys()):
            pedigree = 0
            ofile = output + '/' + chro + '_' + str(tag * int(win)) + '_' + str((tag + 1) * int(win)) + '.ped'
            with open (ofile, 'w') as ofilehd:    
                for samplen in sorted(data[chro][tag].keys()):
                    haplotype = []
                    pedigree  += 1
                    strain    = output + str(samplen)
                    haplotype.append(str(pedigree))
                    haplotype.append(strain)
                    haplotype.extend(['0','0','2','0'])
                    for g in data[chro][tag][samplen]:
                        haplotype.append(g + " " + g)              
                    genotype = "\t".join(haplotype)
                    print >> ofilehd, genotype
            mfile = output + '/' + chro + '_' + str(tag * int(win)) + '_' + str((tag + 1) * int(win)) + '.inf'
            with open (mfile, 'w') as mfilehd:
                for pos in marker[chro][tag]:
                    markern = 'm' + str("%08d" %int(pos))
                    print >> mfilehd, markern + '\t' + pos
            prefix  = output + '/' + chro + '_'  + str(tag * int(win)) + '_' + str((tag + 1) * int(win))
            cmdline = 'java -jar Haploview.jar -nogui -memory 5000 -pedfile ' + ofile + ' -info ' + mfile + ' -out ' + prefix + ' -compressedpng -dprime -maxdistance 50000'
            os.system(cmdline) 



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input')
    parser.add_argument('-w', '--window')
    parser.add_argument('-o', '--output')
    parser.add_argument('-v', dest='verbose', action='store_true')
    args = parser.parse_args()
    try:
        len(args.input) > 0
    except:
        usage()
        sys.exit(2)

    if args.output is None:
        args.output = 'BGI_Jap'
 
    '''Convert the genotype from matrix to ped and inf files for haploview'''
    if args.window is None:
        matrix2haploview(args.input,args.output)
    else:
        matrix2haploview_win(args.input,args.output) 

if __name__ == '__main__':
    main()

