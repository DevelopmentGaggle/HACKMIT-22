Essence - HackMIT-22
====================

Audience and Presenter Natural Language Processing Assistent
---------------------

## Essence Logo
![Logo](logo.png)

Essence is a powerful learning tool that uses Natural Language Processing and speech recognition to assist in audience understanding of presentation topics. It aims to overcome lecture-based learning barriers by providing additional context for the key topics being discussed, and demystifying unfamiliar references to ensure everyone in the audience is on the same page. Moreover, Essence captures and displays images related to key words and phrases to reinforce lecture material and increase engagement of visual learners in lecture-based education environments.

Essence uses the Google speech recognition service to sample microphone audio and convert it to text in real-time. The generated text then passes through 2 different Natural Language Processing tools - YAKE for extracting key words and phrases for topic analysis, and spaCy for determining information about the sentence structure and part of speech of each word. This data is used to extract wikipedia text summaries and relevant bing images to generate informative widgets that provide more details about important topics that were mentioned.

While these threads are run, a cross-platform pyqt GUI is filled with user facing data, such as real time metrics for text density and a word cloud for broad categorization of the topics discussed. These metrics not only aid audience understanding of lecture topics, but also provide valuable insight for the presenter as to how their content is likely to be perceived. This makes Essence the perfect tool for ensuring effective presentations that promote accessibility and engagement for audiences of all backgrounds.


