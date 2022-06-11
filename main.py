from operator import mod
import subprocess
import re

def analyzeDiffCode():
    print('analyze')

def removeAddedLogs():
    for file in modifiedFiles:
        lineNumber = 0
        addedLogs= []
        diffFileName = 'diff-'+ file.split('.')[0] + '.txt'
        print(diffFileName)
        f = open(f'diffs/{diffFileName}', 'r')
        fileContent = f.readlines()
        for line in fileContent:
            lineNumber += 1
            if line[0] == '+':
                if 'console.log' in line[1:]:
                    print(lineNumber)
                    addedLogs.append(line[1:])

if __name__ == '__main__':
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
        process = subprocess.Popen(['mkdir', 'diffs'],
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        splits = decodedResult.split('\n')
        for line in splits:
            if len(line) > 0 and line[0] == '\t':
                    lineSplits = line.split('  ')
                    if lineSplits[0] == '\tnew file:':
                        newlyAddedFiles.append(lineSplits[1].strip(' '))
                    else:
                        if lineSplits[1].strip(' ') != '.gitignore':
                            modifiedFiles.append(lineSplits[1].strip(' '))
        print(f'modified files: "{modifiedFiles}"')
        print(f'newly added files: "{newlyAddedFiles}"')

        for modifiedFile in modifiedFiles:
            outputFileOption = '--output=' + 'diffs/diff-' + modifiedFile.split('.')[0] + '.txt'
            process = subprocess.Popen(['git', 'diff', outputFileOption, modifiedFile],
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            if (stderr):
                print(f'Error: "{stderr}"')
        removeAddedLogs()