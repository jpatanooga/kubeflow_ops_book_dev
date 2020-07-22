import kfserving
#from torchvision import models, transforms
from typing import List, Dict

from transformers import AutoTokenizer, TFAutoModelForQuestionAnswering
import tensorflow as tf

#import torch
#from PIL import Image
import base64
import io


        




class KFServing_BERT_QA_Model(kfserving.KFModel):
    def __init__(self, name: str):
        super().__init__(name)
        self.name = name
        self.ready = False
        self.tokenizer = None

    def load(self):

        self.tokenizer = AutoTokenizer.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")
        self.model = TFAutoModelForQuestionAnswering.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")
        self.ready = True

    def predict(self, request: Dict) -> Dict:
        inputs = request["instances"]

        source_text = inputs[0]["text"]
        questions = inputs[0]["questions"]

        print( source_text )
        print( questions )

        results = {}


        for question in questions:
            print("Processing question: " + question)
            inputs = self.tokenizer.encode_plus(question, source_text, add_special_tokens=True, return_tensors="tf")
            input_ids = inputs["input_ids"].numpy()[0]

            text_tokens = self.tokenizer.convert_ids_to_tokens(input_ids)
            answer_start_scores, answer_end_scores = self.model(inputs)

            answer_start = tf.argmax(
                answer_start_scores, axis=1
            ).numpy()[0]  # Get the most likely beginning of answer with the argmax of the score
            answer_end = (
                tf.argmax(answer_end_scores, axis=1) + 1
            ).numpy()[0]  # Get the most likely end of answer with the argmax of the score
            answer = self.tokenizer.convert_tokens_to_string(self.tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end]))

            print(f"Question: {question}")
            print(f"Answer: {answer}\n")

            results[ question ] = answer


        return {"predictions": results}


if __name__ == "__main__":
    model = KFServing_BERT_QA_Model("kfserving-custom-model")
    model.load()
    kfserving.KFServer(workers=1).start([model])