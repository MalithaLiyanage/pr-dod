from operator import mod
import subprocess
import os
import re
            

def find_changed_files():
    untrackedFiles = []
    newlyAddedFiles = []
    modifiedFiles = []

    process = subprocess.Popen(['git', 'status'],
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if (stderr):
        print(f'Error: "{stderr}"')

    decodedResult = stdout.decode('utf8')

    # isNothingToCommit = 'nothing to commit, working tree clean' in decodedResult
    isUntrackedFilesAvailable = 'Untracked files' in decodedResult

    if (isUntrackedFilesAvailable):
        splits = decodedResult.split('\n');

        for line in splits:
            if len(line) > 0 and line[0] == '\t':
                untrackedFiles.append(line.strip('\t'))

        print(f'untracked files: "{untrackedFiles}"')

        untrackedFilesInput = input(f'Found "{len(untrackedFiles)}" untracked files. Do you want to add all of them? (Y/n)')
        if untrackedFilesInput == 'y' or untrackedFilesInput == 'Y' or untrackedFilesInput == '':
            process = subprocess.Popen(['git', 'add', '.'],
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            if (stderr):
                print(f'Error: "{stderr}"')

    isNoCommitsYet = 'No commits yet' in decodedResult or 'Changes not staged for commit' in decodedResult

    if isNoCommitsYet:

        splits = decodedResult.split('\n')
        for line in splits:
            if len(line) > 0 and line[0] == '\t':
                    lineSplits = line.split('  ')
                    if lineSplits[0] == '\tnew file:':
                        newlyAddedFiles.append(lineSplits[1].strip(' '))
                    else:
                        if lineSplits[1].strip(' ') != '.gitignore':
                            modifiedFiles.append(lineSplits[1].strip(' '))
        modifiedFiles = set(modifiedFiles)
        print(f'modified files: "{modifiedFiles}"')
        print(f'newly added files: "{newlyAddedFiles}"')

if __name__ == '__main__':
    x =subprocess.Popen(['git', 'diff', 'main.py'],  stdout=subprocess.PIPE, 
                         stderr=subprocess.PIPE)
    stdout, stderr = x.communicate()
    if (stderr):
        print(f'Error: "{stderr}"')
    decodedDiffResult = stdout.decode('utf8') 

    for line in decodedDiffResult.split('\n'):
        if(len(line) > 2 and line[0] == '@' and line[1] == '@' and line[len(line) -1] == '@' and line[len(line) -2] == '@'):

            formattedLine = line.split('@@')
            formattedPlusSplits = formattedLine[1].split('+')
            startingLine = formattedPlusSplits[1].split(',')[0]
            noOfAddedLines = formattedPlusSplits[1].split(',')[1]
            print(startingLine)
            print(noOfAddedLines)
    find_changed_files()

