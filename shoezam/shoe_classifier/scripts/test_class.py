from shoezam.shoe_classifier import ShoeClassifier

cnn = ShoeClassifier()
image_path = "/Users/bechtel/Work/Insight/shoezam/webapp/image_test.jpg"
cnn.find_top_matches_by_path(image_path)
#cnn.find_top_matches()
