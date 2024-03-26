import os



def resolve_mult_allele(allele, scheme):
    allele_name = allele.split("(")[0]
    alleles = allele.split('(')[1].split(')')[0].split(',')
    fasta = os.path.join(snakemake.params.mlst_dir, "db", "pubmlst", scheme, allele_name + ".tfa")
    with open(fasta) as f:
        getseq = False
        seqdict = {}
        for line in f:
            if line.startswith(">"):
                getseq = False
                name = line.split()[0].split('_')[-1]
                if name in alleles:
                    getseq = True
                    seqdict[name] = ''
            elif getseq:
                seqdict[name] += line.rstrip().lower()
    out_alleles = set()
    for i in alleles:
        subset = False
        for j in seqdict:
            if seqdict[i] in seqdict[j] and i != j:
                subset = True
                break
        if not subset:
            out_alleles.add(i)
    out_alleles = list(out_alleles)
    out_alleles.sort(key=lambda x: int(x))
    return(allele.split('(')[0] + '(' + ','.join(out_alleles) + ')')


def update_profile(profile, scheme):
    profiles = os.path.join(snakemake.params.mlst_dir, "db", "pubmlst", scheme, scheme + ".txt")
    new_profile = []
    for i in profile:
        new_profile.append(i.split('(')[1].split(')')[0].replace("~", "").replace("?", ""))
    with open(profiles) as f:
        f.readline()
        for line in f:
            splitline = line.rstrip().split("\t")
            if splitline[1:1+len(new_profile)] == new_profile:
                return splitline[0]
    return "-"



headers = ["Sample", "MLST", "abcZ", "adk", "aroE", "fumC", "gdh", "pdhC", "pgm", "NgSTAR", "penA NgSTAR", "penA comment",
           "mtrR NgSTAR", "mtrR comment", "porB NgSTAR", "porB comment", "ponA NgSTAR", "ponA comment",
           "gyrA NgSTAR", "gyrA comment", "parC NgSTAR", "parC comment", "23S NgSTAR", "23S comment", "NgMAST",
           "porB NgMAST", "tbpB", "rplF", "rplF species", "rplf species comment", "rplf_depth", "ppnG coverage", "ppnG depth",
           "23S_bases_pos{}:a:t:g:c".format(snakemake.params.position1), "23S_bases_pos{}:a:t:g:c".format(snakemake.param.position2)]

outstring = snakemake.params.sample
with open(snakemake.input.mlst) as f:
    contig, scheme, profile, abcZ, adk, aroE, fumC, gdh, pdhC, pgm = f.readline().rstrip().split("\t")
    new_profile = []
    for i in [abcZ, adk, aroE, fumC, gdh, pdhC, pgm]:
        if ',' in i:
            new_allele = resolve_mult_allele(i, "mlst")
        else:
            new_allele = i
        new_profile.append(new_allele)
    if new_profile != [abcZ, adk, aroE, fumC, gdh, pdhC, pgm]:
        penA, mtrR, porB, ponA, gyrA, parC, rna23S = new_profile
        profile = update_profile(new_profile, "mlst")


outstring += "\t" + profile
outstring += "\t" + abcZ.split('(')[1].split(')')[0]
outstring += "\t" + adk.split('(')[1].split(')')[0]
outstring += "\t" + aroE.split('(')[1].split(')')[0]
outstring += "\t" + fumC.split('(')[1].split(')')[0]
outstring += "\t" + gdh.split('(')[1].split(')')[0]
outstring += "\t" + pdhC.split('(')[1].split(')')[0]
outstring += "\t" + pgm.split('(')[1].split(')')[0]



with open(snakemake.input.ngstar) as f:
    contig, scheme, profile, penA, mtrR, porB, ponA, gyrA, parC, rna23S = f.readline().rstrip().split("\t")
    new_profile = []
    for i in [penA, mtrR, porB, ponA, gyrA, parC, rna23S]:
        if ',' in i:
            new_allele = resolve_mult_allele(i, "ngstar")
        else:
            new_allele = i
        new_profile.append(new_allele)
    if new_profile != [penA, mtrR, porB, ponA, gyrA, parC, rna23S]:
        penA, mtrR, porB, ponA, gyrA, parC, rna23S = new_profile
        profile = update_profile(new_profile, "ngstar")




comment_dict = {"penA":{"-":"-"}, "mtrR":{"-":"-"}, "porB":{"-":"-"}, "ponA":{"-":"-"}, "gyrA":{"-":"-"}, "parC":{"-":"-"}, "rna23S":{"-":"-"}}
with open(os.path.join(snakemake.params.mlst_dir, "db", "pubmlst", "ngstar", "NEIS1753.tfa.comments")) as f:
    for line in f:
        allele, comment = line.rstrip().split("\t")
        comment_dict["penA"][allele] = comment
with open(os.path.join(snakemake.params.mlst_dir, "db", "pubmlst", "ngstar", "mtrR.tfa.comments")) as f:
    for line in f:
        allele, comment = line.rstrip().split("\t")
        comment_dict["mtrR"][allele] = comment
with open(os.path.join(snakemake.params.mlst_dir, "db", "pubmlst", "ngstar", "NG_porB.tfa.comments")) as f:
    for line in f:
        allele, comment = line.rstrip().split("\t")
        comment_dict["porB"][allele] = comment
with open(os.path.join(snakemake.params.mlst_dir, "db", "pubmlst", "ngstar", "NG_ponA.tfa.comments")) as f:
    for line in f:
        allele, comment = line.rstrip().split("\t")
        comment_dict["ponA"][allele] = comment
with open(os.path.join(snakemake.params.mlst_dir, "db", "pubmlst", "ngstar", "NG_gyrA.tfa.comments")) as f:
    for line in f:
        allele, comment = line.rstrip().split("\t")
        comment_dict["gyrA"][allele] = comment
with open(os.path.join(snakemake.params.mlst_dir, "db", "pubmlst", "ngstar", "NG_parC.tfa.comments")) as f:
    for line in f:
        allele, comment = line.rstrip().split("\t")
        comment_dict["parC"][allele] = comment
with open(os.path.join(snakemake.params.mlst_dir, "db", "pubmlst", "ngstar", "NG_23S.tfa.comments")) as f:
    for line in f:
        allele, comment = line.rstrip().split("\t")
        comment_dict["rna23S"][allele] = comment


outstring += "\t" + profile


allele = penA.split('(')[1].split(')')[0]
outstring += "\t" + allele
comment = []
for i in allele.split(','):
    comment.append(comment_dict["penA"][i.replace("~", "").replace("?", "")])
outstring += "\t" + ",".join(comment)

allele = mtrR.split('(')[1].split(')')[0]
outstring += "\t" + allele
comment = []
for i in allele.split(','):
    comment.append(comment_dict["mtrR"][i.replace("~", "").replace("?", "")])
outstring += "\t" + ",".join(comment)

allele = porB.split('(')[1].split(')')[0]
outstring += "\t" + allele
comment = []
for i in allele.split(','):
    comment.append(comment_dict["porB"][i.replace("~", "").replace("?", "")])
outstring += "\t" + ",".join(comment)

allele = ponA.split('(')[1].split(')')[0]
outstring += "\t" + allele
comment = []
for i in allele.split(','):
    comment.append(comment_dict["ponA"][i.replace("~", "").replace("?", "")])
outstring += "\t" + ",".join(comment)

allele = gyrA.split('(')[1].split(')')[0]
outstring += "\t" + allele
comment = []
for i in allele.split(','):
    comment.append(comment_dict["gyrA"][i.replace("~", "").replace("?", "")])
outstring += "\t" + ",".join(comment)

allele = parC.split('(')[1].split(')')[0]
outstring += "\t" + allele
comment = []
for i in allele.split(','):
    comment.append(comment_dict["parC"][i.replace("~", "").replace("?", "")])
outstring += "\t" + ",".join(comment)

allele = rna23S.split('(')[1].split(')')[0]
outstring += "\t" + allele
comment = []
for i in allele.split(','):
    comment.append(comment_dict["rna23S"][allele.replace("~", "").replace("?", "")])
outstring += "\t" + ",".join(comment)


with open(snakemake.input.ngmast) as f:
    contig, scheme, profile, porB, tbpB = f.readline().rstrip().split("\t")
    new_profile = []
    for i in [porB, tbpB]:
        if ',' in i:
            new_allele = resolve_mult_allele(i, "ngmast")
        else:
            new_allele = i
        new_profile.append(new_allele)
    if new_profile != [porB, tbpB]:
        porB, tbpB = new_profile
        profile = update_profile(new_profile, "ngmast")




outstring += "\t" + profile
outstring += "\t" + porB.split('(')[1].split(')')[0]
outstring += "\t" + tbpB.split('(')[1].split(')')[0]

rplf_dict = {}
with open(os.path.join(snakemake.params.mlst_dir, "db", "pubmlst", "rplf", "rplf.txt")) as f:
    for line in f:
        profile, rplf, species, comment = line.rstrip().split("\t")
        rplf_dict[profile] = [profile, species, comment]


with open(snakemake.input.rplf) as f:
    fasta, scheme, profile, rplf = f.readline().rstrip().split("\t")


if profile in rplf_dict:
    outstring += "\t" + "\t".join(rplf_dict[profile])
else:
    outstring += "\t" + profile + "\tmissing\tmissing"

with open(snakemake.input.rplf_cov) as f:
    f.readline()
    cov = f.readline().rstrip().split()[1]
    depth = f.readline().rstrip().split()[1]

outstring +=  "\t" + depth


with open(snakemake.input.ppng_cov) as f:
    f.readline()
    cov = f.readline().rstrip().split()[1]
    depth = f.readline().rstrip().split()[1]

outstring += "\t" + cov + "\t" + depth

with open(snakemake.input.rrna_alleles) as f:
    f.readline()
    pos, a, t, g, c = f.readline().split()
    outstring += "\t{}:{}:{}:{}".format(a,t,g,c)
    pos, a, t, g, c = f.readline().split()
    outstring += "\t{}:{}:{}:{}".format(a,t,g,c)


with open(snakemake.output.tsv, 'w') as o:
    o.write("\t".join(headers) + "\n")
    o.write(outstring + "\n")