from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from emotion_detection import Emotion


if __name__ == '__main__':
    emotion = Emotion()

    emotion.read_dataset()

    emotion.train_model()


    chatbot = ChatBot("Chatbot")

    trainer = ChatterBotCorpusTrainer(chatbot)

    trainer.train(
        "chatterbot.corpus.english"
    )

    exit_conditions = (":q", "quit", "exit")
    while True:
        query = input("> ")
        if query in exit_conditions:
            break
        else:
            print(f"\nprediction: {emotion.prediction(query)}\n")
            print(f"🤖 {chatbot.get_response(query)}")


