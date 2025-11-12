
import os
import shutil
def delete_folder_contents(folder_path):
    if not os.path.exists(folder_path):
        return

    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path):
            os.remove(item_path)
        else:
            shutil.rmtree(item_path)

if __name__ == "__main__":
    folder_path = 'D:/agent_files'
    delete_folder_contents(folder_path)