from operator import mod
import subprocess
import re

untrackedFiles = []
newlyAddedFiles = []
modifiedFiles = []

process = subprocess.Popen(['git', 'status'],
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)
stdout, stderr = process.communicate()

decodedResult = stdout.decode('utf8')

if (stderr):
    print(f'Error: "{stderr}"')
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

isNoCommitsYet = 'No commits yet' in decodedResult

if isNoCommitsYet:
    splits = decodedResult.split('\n')
    for line in splits:
        if len(line) > 0 and line[0] == '\t':
                lineSplits = line.split('  ')
                if lineSplits[0] == '\tnew file:':
                    newlyAddedFiles.append(lineSplits[1].strip(' '))
                else:
                    modifiedFiles.append(lineSplits[1].strip(' '))
    print(f'modified files: "{modifiedFiles}"')
    print(f'newly added files: "{newlyAddedFiles}"')