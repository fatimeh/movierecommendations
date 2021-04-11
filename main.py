"""CSC111 Winter 2021 Final Project

Overview and Description
========================

This Python module contains the main runner function for the
movie recommendation system.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited.

This file is Copyright (c) 2021 Fatimeh Hassan, Shilin Zhang,
Dorsa Molaverdikhani, and Nimit Bhanshali.
"""
from __future__ import annotations
from entities import Movie, _MovieVertex, MovieGraph
from visualization import main_runner

# Main runner function
GENRES = ['Western', 'Family', 'Adventure', 'War', 'Fantasy', 'History', 'Music', 'Documentary',
          'Reality-TV', 'Animation', 'Sport', 'Action', 'Mystery', 'Crime', 'Drama', 'Horror',
          'Film-Noir', 'Musical', 'Comedy', 'Adult', 'Romance', 'Sci-Fi', 'Biography', 'News',
          'Thriller']
LANGUAGES = ['Quechua', 'Gujarati', 'Kabyle', 'Mari', 'Filipino', 'Mongolian', 'Aramaic', 'Songhay',
             'Afrikaans', 'English', 'Crimean Tatar', 'Sicilian', 'American Sign Language',
             'Nenets', 'Ladino', 'Tupi', 'Sranan', 'Australian Sign Language', 'Balinese',
             'Southern Sotho', 'Spanish', 'Creek', 'Mende', 'Tajik', 'Maori',
             'North American Indian', 'Mandingo', 'Cheyenne', 'Neapolitan', 'Maltese', 'Oriya',
             'Catalan', 'German', 'Navajo', 'Tigrigna', 'Kabuverdianu', 'Korean', 'Bambara',
             'Dutch', 'Hindi', 'Rajasthani', 'Shona', 'Occitan', 'Slovenian', 'Sioux', 'Swedish',
             'Uzbek', 'Icelandic', 'Peul', 'Teochew', 'Bhojpuri', 'Nepali', 'Micmac', 'Min Nan',
             'Wolof', 'Lithuanian', 'Rhaetian', 'Spanish Sign Language', 'Arapaho', 'Hakka',
             'Shanghainese', 'Faroese', 'Serbian', 'Haida', 'Pawnee', 'Kriolu', 'Sinhalese',
             'Washoe', 'Quenya', 'Tswana', 'Finnish', 'Urdu', 'Algonquin', 'Acholi', 'Portuguese',
             'Russian Sign Language', 'Indonesian', 'Marathi', 'Low German', 'Ibo',
             'Egyptian (Ancient)', 'Estonian', 'Gumatj', 'Mandarin', 'Nyanja', 'Abkhazian',
             'Chinese', 'Mixtec', 'Norse', 'British Sign Language', 'Purepecha', 'Hopi',
             'Greenlandic', 'Flemish', 'Guarani', 'Crow', 'Georgian', 'Hassanya', 'Sign Languages',
             'Polynesian', 'Japanese Sign Language', 'Tarahumara', 'Yoruba', 'Turkish', 'Sindhi',
             'Frisian', 'Latin', 'Scottish Gaelic', 'Chechen', 'Dzongkha', 'Manipuri', 'Pushto',
             'Korean Sign Language', 'Cornish', 'Haitian', 'Apache languages', 'Bable', 'Nama',
             'Xhosa', 'Romany', 'Persian', 'Scanian', 'Irish', 'Zulu', 'Eastern Frisian', 'Soninke',
             'Vietnamese', 'Indian Sign Language', 'Kikuyu', 'Ryukyuan', 'Haryanvi', 'Latvian',
             'Kalmyk-Oirat', 'Ladakhi', 'Khanty', 'Malay', 'Croatian', 'Konkani', 'Rotuman',
             'Malayalam', 'Albanian', 'Breton', 'Papiamento', 'Kashmiri', 'Somali', 'Russian',
             'Dari', 'Ojibwa', 'Bengali', 'Yakut', 'Welsh', 'Sindarin', 'Tamashek', 'Hawaiian',
             'Thai', 'Cree', 'Kuna', 'Esperanto', 'Raeto-Romance', 'Ukrainian Sign Language',
             'Yiddish', 'Polish', 'Swiss German', 'Greek', 'Tamil', 'Samoan', 'Tagalog', 'Maithili',
             'Kru', 'Parsee', 'Slovak', 'Hungarian', 'Punjabi', 'Tatar', 'More', 'Berber languages',
             'Wayuu', 'Minangkabau', 'Hokkien', 'Visayan', 'Scots', 'Tibetan', 'Shoshoni',
             'Mirandese', 'Malinka', 'Old English', 'Hebrew', 'Danish', 'Tonga', 'French',
             'Japanese', 'Mohawk', 'Ewe', 'Kirghiz', 'French Sign Language', 'Lao', 'Cantonese',
             'Amharic', 'Montagnais', 'Sardinian', 'Czech', 'Nahuatl', 'Old', 'Mapudungun',
             'Awadhi', 'Kinyarwanda', 'Inuktitut', 'Serbo-Croatian', 'Aboriginal', 'Assamese',
             'Lingala', 'Norwegian', 'Kirundi', 'Dinka', 'Khmer', 'Ukrainian', 'Akan', 'Maya',
             'Hausa', 'Uighur', 'Aromanian', 'Brazilian Sign Language', 'Klingon', 'Gallegan',
             'Arabic', 'Central American Indian languages', 'Ancient (to 1453)', 'Armenian',
             'Fulah', 'Kazakh', 'Azerbaijani', 'Basque', 'Sanskrit', 'German Sign Language',
             'Bicolano', 'Luxembourgish', 'Corsican', 'Dyula', 'Tulu', 'None', 'Romanian',
             'Himachali', 'Kurdish', 'Italian', 'Belarusian', 'Bemba', 'Swahili', 'Burmese',
             'Bosnian', 'Kannada', 'Hmong', 'Pular', 'Aragonese', 'Tok Pisin',
             'Athapascan languages', 'Macedonian', 'Syriac', 'Assyrian Neo-Aramaic', 'Telugu',
             'Tzotzil', 'Bulgarian', 'Turkmen', 'Middle English', 'Shanxi', 'Aymara', 'Ungwatsi',
             'Saami']
