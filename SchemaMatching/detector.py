from abc import abstractmethod
import re
import numpy as np
from sklearn.ensemble import RandomForestClassifier

class field_matcher:
    def __init__(self, valid_weight, constrain_weight):
        self.valid_weight = valid_weight
        self.contrain_weight = constrain_weight

    @abstractmethod
    def evaluated(self, list_elements):
        return NotImplementedError

    @abstractmethod
    def check_constrain_element(self, element):
        return NotImplementedError

    @abstractmethod
    def train(self, X_texts, X_features, y_category):
        return NotImplementedError

class detector(field_matcher):
    def __init__(self, valid_weight, constrain_weight):
        super(detector, self).__init__(valid_weight, constrain_weight)

    @abstractmethod
    def check_valid_element(self, element):
        return NotImplementedError

    def check_element(self, element):
        return self.valid_weight*self.check_valid_element(element) + \
               self.contrain_weight*self.check_constrain_element(element)

    def train(self, X_texts, X_features, y_category):
        return None

    def evaluated(self, list_elements):
        element_scores = [self.check_element(element) for element in list_elements]
        return np.mean(element_scores)

class property_date_detector(detector):
    def __init__(self, valid_weight = 1, constrain_weight = 0):
        super(property_date_detector, self).__init__(valid_weight, constrain_weight)

    def check_valid_element(self, element):
        if isinstance(element, str):
            if re.match("^(\d{2}/\d{2}/\d{4})$", element):
                return 1
            else:
                return 0
        else:
            return 0

    def check_constrain_element(self, element):
        return 1

class property_link_detector(detector):
    def __init__(self, valid_weight = 1, constrain_weight = 0):
        super(property_link_detector, self).__init__(valid_weight, constrain_weight)

    def check_valid_element(self, element):
        if isinstance(element, str):
            if re.match("^(http)\S*(\.html)$", element):
                return 1
            else:
                return 0
        else:
            return 0

    def check_constrain_element(self, element):
        return 1

class property_images_detector(detector):
    def __init__(self, valid_weight = 1, constrain_weight = 0):
        super(property_images_detector, self).__init__(valid_weight, constrain_weight)

    def check_valid_element(self, element):
        if isinstance(element, list):
            score = []
            for e in element:
                if isinstance(e, str):
                    if re.match("^(http)\S*((\.jpg)|(\.png))$", e):
                        score.append(1)
                    else:
                        score.append(0)
                else:
                    score.append(0)
            if len(score) == 0:
                return 0
            else:
                return np.mean(score)
        else:
            return 0

    def check_constrain_element(self, element):
        return 1

class classifier(field_matcher):
    def __init__(self, valid_weight, constrain_weight, feature_extractor, category):
        super(classifier, self).__init__(valid_weight, constrain_weight)
        self.category = category
        self.feature_extractor = feature_extractor
        self.classifer = None
        self.lower_length = None
        self.upper_length = None

    def train(self, X_texts, X_features, y_category):
        y_binary = y_category == self.category
        y_binary = y_binary.astype(int)
        self.classifer = RandomForestClassifier()
        self.classifer.fit(X_features, y_binary)

        text_lengths = [len(text) for text in X_texts[y_category == self.category]]
        self.lower_length, self.upper_length = np.percentile(text_lengths, [10, 90])

    def check_constrain_element(self, element):
        if len(element)>=self.lower_length and len(element)<=self.upper_length:
            return 1
        else:
            return 0

    def predict(self, list_elements):
        X_features = self.feature_extractor.transform(list_elements)
        y_predict = self.classifer.predict(X_features)
        return y_predict

    def evaluated(self, list_elements):
        valid_elements = []
        contrain_scores = []
        for element in list_elements:
            if isinstance(element, str):
                valid_elements.append(element)
                contrain_scores.append(self.check_constrain_element(element))
        if len(valid_elements) > 0:
            predict_labels = self.predict(valid_elements)
            return (np.sum(predict_labels)*self.valid_weight+np.sum(contrain_scores)*self.contrain_weight)/len(list_elements)
        else:
            return 0

class property_title_classifier(classifier):
    def __init__(self, valid_weight = 0.8, constrain_weight = 0.2, feature_extractor = None, category = 0):
        super(property_title_classifier, self).__init__(valid_weight, constrain_weight, feature_extractor, category)

class property_detail_classifier(classifier):
    def __init__(self, valid_weight = 0.8, constrain_weight = 0.2, feature_extractor = None, category = 1):
        super(property_detail_classifier, self).__init__(valid_weight, constrain_weight, feature_extractor, category)

class property_price_classifier(classifier):
    def __init__(self, valid_weight = 0.5, constrain_weight = 0.5, feature_extractor = None, category = 2):
        super(property_price_classifier, self).__init__(valid_weight, constrain_weight, feature_extractor, category)

    def check_constrain_element(self, element):
        if len(element)>=self.lower_length and len(element)<=self.upper_length and re.match("^\s*\d+([\.,]\d+)?\s*((tỷ)|(triệu)|(tr))\s*$", element):
            return 1
        else:
            return 0


class property_area_classifer(classifier):
    def __init__(self, valid_weight = 0.5, constrain_weight = 0.5, feature_extractor = None, category = 3):
        super(property_area_classifer, self).__init__(valid_weight, constrain_weight, feature_extractor, category)

    def check_constrain_element(self, element):
        if len(element) >= self.lower_length and len(element) <= self.upper_length and re.match("^\s*\d+((ha)|(M\s*2)|(m\s*2))\s*$", element):
            return 1
        else:
            return 0

class property_address_classifer(classifier):
    def __init__(self, valid_weight = 1, constrain_weight = 0, feature_extractor = None, category = 4):
        super(property_address_classifer, self).__init__(valid_weight, constrain_weight, feature_extractor, category)

class property_type_classifer(classifier):
    def __init__(self, valid_weight = 1, constrain_weight = 0, feature_extractor = None, category = 5):
        super(property_type_classifer, self).__init__(valid_weight, constrain_weight, feature_extractor, category)
