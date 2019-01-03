# shoezam

This is the project repo for Shoezam a shoe identification and recommendation app at [shoezam.online](shoezam.online). 

<video width="320" height="240" controls>
  <source src="Shoezam_Vid.mov" type="video/mp4">
</video>

The project consists of three parts: 

1. zap_scrap: a web scraping tool built using Selenium and BeautifulSoup,
2. ShoeClassifier: a pretrained Keras deep convolutional neural net which identifies similarity between an input image, and an image of a shoe in the database,
3. the web app which includes the dash/flask frontend
