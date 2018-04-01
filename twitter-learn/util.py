from xml.etree import ElementTree

def merge_tweets(xml_test_tagged, xml_test):
    
    root_tagged = ElementTree.parse(xml_test_tagged).getroot()
    root_test = ElementTree.parse(xml_test).getroot()

    for tweet in root_tagged.iter('tweet'):
        tweet_id = int(tweet.find('tweetid').text)

        for tweet_test in root_test.iter('tweet'):
            tweet_test_id = int(tweet_test.find('tweetid').text)

            if tweet_id == tweet_test_id:
                content = tweet_test.find('content')
                tweet.append(content)
                root_test.remove(tweet_test)
                break

    file_handle = open("filename.xml","wb")
    tree = ElementTree.ElementTree(root_tagged)
    tree.write(file_handle)
    file_handle.close()

if __name__ == "__main__":
    import sys

    xml_test_tagged_path = sys.argv[1]
    xml_test_path = sys.argv[2]

    merge_tweets(xml_test_tagged_path, xml_test_path)