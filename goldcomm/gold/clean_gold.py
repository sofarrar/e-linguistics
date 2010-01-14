import re



if __name__=='__main__':
    

    #removes all examples from ontology
    filename='/home/farrar/svn_projects/GOLDComm/gold/gold-2008.owl'

    file=open(filename,'r')

    unclean=file.read()


    regex=re.compile('<gold:hasExample.*?</gold:hasExample>',re.DOTALL)
    replacement=r' '
    noegs=re.sub(regex, replacement, unclean)


    outfile=open('/home/farrar/svn_projects/GOLDComm/gold/gold_no_egs.owl','w')
    outfile.write(noegs)

    outfile.close()




    """
    filename='/home/farrar/svn_projects/GOLDComm/gold/gold_ex.owl'

    file=open(filename,'r')

    unclean=file.read()

    regex=re.compile(r'gold#')
    replacement=r'gold/'
    unclean=re.sub(regex, replacement, unclean)


    regex=re.compile(r'="/')
    replacement=r'="&gold;'
    clean=re.sub(regex, replacement, unclean)


    
    outfile=open('/home/farrar/svn_projects/GOLDComm/gold/gold_ex_cleaned.owl','w')
    outfile.write(clean)

    outfile.close()

    """












