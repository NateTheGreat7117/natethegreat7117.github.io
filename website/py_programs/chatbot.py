from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


language_tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
language_model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium").to(device)

model_path = "/home/nathanmon/Artificial Intelligence/PyTorch/Natural Language Processing/Chatbot/checkpoints/"
# model_ckpt = torch.load(f"{model_path}/best_causal_model.pth")
model_ckpt = torch.load(f"{model_path}/finetuned_1.pth")
language_model.load_state_dict(model_ckpt['model_state_dict'])


def evaluate(text, max_len=25):
    tokenized = language_tokenizer.encode_plus(text,
                                      return_tensors="pt")['input_ids']

    max_len = 25
    for i in range(max_len):
        out = language_model(tokenized.clone().detach().to("cuda"))
        new = torch.argmax(out[0], 2)[0][-1]
        tokenized = torch.unsqueeze(torch.concat((tokenized[0], torch.tensor([new]))), 0)
        if tokenized[0][-2] == 1220 and tokenized[0][-1] == 83:
            break

    return language_tokenizer.decode(tokenized[0])