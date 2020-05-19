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
        #f = open('imagenet_classes.txt')
        #self.classes = [line.strip() for line in f.readlines()]

        #model = models.alexnet(pretrained=True)
        #model.eval()
        #self.model = model

        self.tokenizer = AutoTokenizer.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")
        self.model = TFAutoModelForQuestionAnswering.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")





        self.ready = True

    def predict(self, request: Dict) -> Dict:
        inputs = request["instances"]

        # Input follows the Tensorflow V1 HTTP API for binary values
        # https://www.tensorflow.org/tfx/serving/api_rest#encoding_binary_values
        """
        data = inputs[0]["image"]["b64"]

        raw_img_data = base64.b64decode(data)
        input_image = Image.open(io.BytesIO(raw_img_data))

        preprocess = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225]),
        ])

        input_tensor = preprocess(input_image)
        input_batch = input_tensor.unsqueeze(0)
        """

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


        #output = self.model(input_batch)

        #scores = torch.nn.functional.softmax(output, dim=1)[0]

        #_, top_5 = torch.topk(output, 5)

        #for idx in top_5[0]:
        #    results[self.classes[idx]] = scores[idx].item()
        

        return {"predictions": results}


if __name__ == "__main__":
    model = KFServing_BERT_QA_Model("kfserving-bert-qa-model")
    model.load()
    kfserving.KFServer(workers=1).start([model])