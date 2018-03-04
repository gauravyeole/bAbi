
import os
import zipfile
import tarfile



def download_glove():
    glove_zip_file = "glove.6B.zip"
    glove_vectors_file = "glove.6B.50d.txt"
    try:
        from urllib.request import urlretrieve, urlopen
    except ImportError:
        from urllib import urlretrieve
        from urllib2 import urlopen
    # large file - 862 MB
    if (not os.path.isfile(glove_zip_file) and
            not os.path.isfile(glove_vectors_file)):
        urlretrieve("http://nlp.stanford.edu/data/glove.6B.zip",
                    glove_zip_file)


def download_dataset():
    # 15 MB
    data_set_zip = "tasks_1-20_v1-2.tar.gz"

    # Select "task 5"
    train_set_file = "qa5_three-arg-relations_train.txt"
    test_set_file = "qa5_three-arg-relations_test.txt"

    train_set_post_file = "tasks_1-20_v1-2/en/" + train_set_file
    test_set_post_file = "tasks_1-20_v1-2/en/" + test_set_file
    if (not os.path.isfile(data_set_zip) and
            not (os.path.isfile(train_set_file) and os.path.isfile(test_set_file))):
        urlretrieve("https://s3.amazonaws.com/text-datasets/babi_tasks_1-20_v1-2.tar.gz",
                    data_set_zip)


def unzip_single_file(zip_file_name, output_file_name):
    """
        If the output file is already created, don't recreate
        If the output file does not exist, create it from the zipFile
    """
    if not os.path.isfile(output_file_name):
        with open(output_file_name, 'wb') as out_file:
            with zipfile.ZipFile(zip_file_name) as zipped:
                for info in zipped.infolist():
                    if output_file_name in info.filename:
                        with zipped.open(info) as requested_file:
                            out_file.write(requested_file.read())
                            return


def targz_unzip_single_file(zip_file_name, output_file_name, interior_relative_path):
    if not os.path.isfile(output_file_name):
        with tarfile.open(zip_file_name) as un_zipped:
            un_zipped.extract(interior_relative_path + output_file_name)


def main():
    download_glove()
    download_dataset()
    unzip_single_file(glove_zip_file, glove_vectors_file)
    targz_unzip_single_file(data_set_zip, train_set_file, "tasks_1-20_v1-2/en/")
    targz_unzip_single_file(data_set_zip, test_set_file, "tasks_1-20_v1-2/en/")


if __name__ == "__main__":
    main()
