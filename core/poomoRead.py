def poomoRead(poomo):
    # Check Magic
    poomo.seek(0)
    if poomo.read(4) != b'PUMO':
        print("Poomo has Invalid Magic")
        exit(1)

    # Read Codebook
    codebook = []

    # Block A
    poomo.seek(100)
    codebookAddTmp = list(poomo.read(256))
    if sum(codebookAddTmp) != 32640:
        print("Poomo Block A Sum Error")
        exit(1)
    else:
        codebook += codebookAddTmp

    # Block B
    poomo.seek(400)
    codebookAddTmp = list(poomo.read(256))
    if sum(codebookAddTmp) != 32640:
        print("Poomo Block B Sum Error")
        exit(1)
    else:
        codebook += codebookAddTmp

    # Block C
    poomo.seek(700)
    codebookAddTmp = list(poomo.read(256))
    if sum(codebookAddTmp) != 32640:
        print("Poomo Block C Sum Error")
        exit(1)
    else:
        codebook += codebookAddTmp

    # Block D
    poomo.seek(1000)
    codebookAddTmp = list(poomo.read(256))
    if sum(codebookAddTmp) != 32640:
        print("Poomo Block D Sum Error")
        exit(1)
    else:
        codebook += codebookAddTmp

    return codebook
