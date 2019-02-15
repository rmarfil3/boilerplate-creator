import os
import shutil
import sys


def _logpath(path, names):
    print 'Working in ' + path
    return []   # nothing will be ignored


def merge_folders(root_src_dir, root_dst_dir):
    """Recursively merge two folders including subfolders
    https://lukelogbook.tech/2018/01/25/merging-two-folders-in-python/
    """
    for src_dir, dirs, files in os.walk(root_src_dir):
        dst_dir = src_dir.replace(root_src_dir, root_dst_dir, 1)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        for file_ in files:
            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst_dir, file_)
            if os.path.exists(dst_file):
                os.remove(dst_file)
            shutil.copy(src_file, dst_dir)


def run(*modules):
    """
    :type modules: str
    """
    output_dir = "output"
    source_root_dir = "app"

    try:
        shutil.rmtree(output_dir)
    except:
        pass
    os.mkdir(output_dir)

    print "Building from base..."
    merge_folders("{}/base".format(source_root_dir), output_dir)

    for module in modules:
        print "Inserting module: {}...".format(module)
        merge_folders("{}/{}".format(source_root_dir, module),
                      output_dir)

    print "Build done!"


if __name__ == "__main__":
   run(*sys.argv[1:])
