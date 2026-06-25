from app.ml.predictor import Predictor

class FieldMapper:
    @staticmethod
    def map_labels(labels: list) -> tuple:
        """
        Translates a list of unknown labels into standardized schema mappings and confidence scores.
        Returns a tuple of (mappings_dict, confidences_dict).
        """
        if not labels:
            return {}, {}
            
        # Get batch predictions
        predictions = Predictor.predict_batch(labels)
        
        mappings = {}
        confidences = {}
        
        for label, (pred_class, conf) in zip(labels, predictions):
            mappings[label] = pred_class
            confidences[label] = conf
            
        return mappings, confidences
