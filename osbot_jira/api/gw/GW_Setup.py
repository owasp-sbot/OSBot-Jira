from pbx_gs_python_utils.utils.Files import Files
from osbot_aws.apis.S3               import S3


# this is currently hardcoded for GW environment:
# todo: make this generic (refactor into api)
def load_dependency(target):
    import shutil
    import sys
    s3         = S3()
    s3_bucket  = 'gw-bot-lambdas'
    s3_key     = 'lambdas-dependencies/{0}.zip'.format(target)
    tmp_dir    = Files.path_combine('/tmp/lambdas-dependencies', target)

    if s3.file_exists(s3_bucket,s3_key) is False:
        raise Exception("In Lambda load_dependency, could not find dependency for: {0}".format(target))

    if Files.not_exists(tmp_dir):                               # if the tmp folder doesn't exist it means that we are loading this for the first time (on a new Lambda execution environment)
        zip_file = s3.file_download(s3_bucket, s3_key,False)    # download zip file with dependencies
        shutil.unpack_archive(zip_file, extract_dir = tmp_dir)  # unpack them
        sys.path.append(tmp_dir)                                # add tmp_dir to the path that python uses to check for dependencies

    return tmp_dir
    return Files.exists(tmp_dir)