from db import similarity_search

folderpath = 'C:/Users/User/Documents/GAD/50-query-set/50'
radius = 0.5

successes = [0, 0, 0, 0, 0]
anysuccesses = 0

for file in range(50):
    full_file_path = folderpath + "/" + i + ".mp3"
    result: list = similarity_search(full_file_path, radius)
    for i in range(5):
        if result[i].filename == file + "-" + i + ".mp3":
            successes[i] = successes[i] + 1
        if "" + file + "-" in result[i].filename:
            anysuccesses[i] = anysuccesses[i] + 1
  
print(f"Total success rate: {str(sum(successes) / 250 * 100)}%")
print(f"First five without order success rate: {str(anysuccesses / 250 * 100)}%")
print(f"1st place success rate: {str(successes[0] / 50 * 100)}%")
print(f"2nd place success rate: {str(successes[1] / 50 * 100)}%")
print(f"3rd place success rate: {str(successes[2] / 50 * 100)}%")
print(f"4th place success rate: {str(successes[3] / 50 * 100)}%")
print(f"5th place success rate: {str(successes[4] / 50 * 100)}%")