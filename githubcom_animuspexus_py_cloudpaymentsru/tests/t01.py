import githubcom_animuspexus_py_cloudpaymentsru.client


def main():
    c = githubcom_animuspexus_py_cloudpaymentsru.client.Client(
        basic_auth_user="test",
        basic_auth_password="test"
    )
    print(c.Test())


main()
