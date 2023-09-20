import os
import git
import re


def main():
    create_netrc_file()
    repo = git.Repo('.')

    latest_tag = get_latest_tag(repo)
    should_increment_major = has_major_version(repo, latest_tag)

    [major, minor] = latest_tag.split(".")

    if should_increment_major:
        major = int(major) + 1
        minor = 0
    else:
        minor = int(minor) + 1

    new_tag = create_tag(repo, major, minor)
    write_to_tags_file(new_tag)


def create_netrc_file():
    try:
        machine = os.environ['DRONE_NETRC_MACHINE']
        username = os.environ['DRONE_NETRC_USERNAME']
        password = os.environ['DRONE_NETRC_PASSWORD']
        file_path = f"{os.path.expanduser('~')}/.netrc"

        with open(file_path, "a") as file:
            file.writelines(f"""machine {machine}
login {username}
password {password}""")

    except KeyError:
        print("netrc environment variables do not exist")


def get_latest_tag(repo):
    # Need to fetch the tags from origin as drone does fetch pull them by default
    repo.remote().fetch(tags=True)
    tagBlob = repo.git.ls_remote("origin", "*.*", tags=True, sort="v:refname")
    # Example output of tagBlob
    # 821c5630403683ec0e3d56d3f7018efbe4274839        refs/tags/12.0
    # 821c5630403683ec0e3d56d3f7018efbe4274839        refs/tags/11.1

    autotag_regex = re.compile(r'^\d+\.\d+$')
    all_tags = list(map(lambda ref: ref.split('/')[-1], tagBlob.split('\n')))
    valid_tags = list(filter(autotag_regex.search, all_tags))
    latest_tag = valid_tags[-1]
    print(f'Found latest tag: {latest_tag}')
    return latest_tag


def has_major_version(repo, latest_tag):
    minorStrings = os.environ.get('PLUGIN_MINOR_COMMIT_STRING_CSV', '#autodeploy').split(",")

    for commit in repo.iter_commits(rev=f'{latest_tag}..HEAD', no_merges=True):
        print(f'Checking commit: {commit}')
        if not any(map(commit.message.__contains__, minorStrings)):
            print(f'Found major commit message: {commit.message}')
            return True
    print('No major commit message found')
    return False


def create_tag(repo, major, minor):
    tag_name = f"{major}.{minor}"
    tag = repo.create_tag(tag_name)
    repo.remote('origin').push(tag.path)
    print(f'Tag created: {tag_name}')
    return tag_name


def write_to_tags_file(new_tag):
    drone_build_number = os.environ['DRONE_BUILD_NUMBER']
    image_prefix = os.environ.get('PLUGIN_IMAGE_PREFIX', '')
    docker_image_tag = f'{image_prefix}{drone_build_number}-{new_tag}'
    with open(".tags", "a") as file:
        is_empty_file = file.tell() == 0
        if not is_empty_file:
            file.write(",")
        file.write(docker_image_tag)
    print(f'Docker tag written to .tags: {docker_image_tag}')


main()

# Test change 1
