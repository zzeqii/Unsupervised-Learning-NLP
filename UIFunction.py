import TopicModel
import notionUI
import sys
import time
from Json_to_csv import json_to_csv

MODEL = None

def center(QW):
    qr = QW.frameGeometry()
    cp = notionUI.QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    QW.move(qr.topLeft())

def find_doc(model,topic_id,doc_index):
    doc_id = model.topic_doc.iloc[topic_id,1].split(',')[doc_index]
    return list(model.doc_topic[model.doc_topic.doc_id == int(doc_id)]['content'])[0]


#choose feature to use
def choose(QW):
    global MODEL
    function = QW.sender().text()
    if function == 'Train Model':
        train_model(QW)

    if function == 'Load Model':
        load_model(QW)

    if function == 'Updata Model':
        if MODEL == None:
            notionUI.QMessageBox.warning(QW,'Message','There is no model yet, please load or train model first.',notionUI.QMessageBox.Ok,notionUI.QMessageBox.Ok)
        else:
            update_model(QW)

    if function == 'Save Model':
        if MODEL == None:
            notionUI.QMessageBox.warning(QW,'Message','There is no model yet, please load or train model first.',notionUI.QMessageBox.Ok,notionUI.QMessageBox.Ok)
        else:
            save_model(QW)

    if function == 'View Model':
        if MODEL == None:
            notionUI.QMessageBox.warning(QW,'Message','There is no model yet, please load or train model first.',notionUI.QMessageBox.Ok,notionUI.QMessageBox.Ok)
        else:
            view_model(QW)

def train_model(QW):
    global MODEL
    filewindow = notionUI.FileWindow()
    filewindow.setWindowTitle('choose training data')
    if filewindow.exec_():
        if filewindow.path == '':
            notionUI.QMessageBox.warning(QW, 'Message', 'Please choose a folder.', notionUI.QMessageBox.Ok, notionUI.QMessageBox.Ok)
        else:
            path = filewindow.path

        trainwindow = notionUI.TrainWindow()
        if trainwindow.exec_():
            model = trainwindow.m_bt.currentText().lower()
            iter = trainwindow.le1.text()
            num_topics = trainwindow.le2.text()
            ngram = trainwindow.c1.isChecked()
            lemma = trainwindow.c2.isChecked()
            sw = trainwindow.c3.isChecked()
            tfidf = trainwindow.c4.isChecked()

            if not json_to_csv(path):
                notionUI.QMessageBox.warning(filewindow, 'Waring', 'There is no training data, please choose another folder')
                return
            else:
                QW.pwindow = notionUI.ProgressWindow()
                QW.pwindow.show()
                print(model,iter,num_topics,ngram,lemma,sw,tfidf)
                MODEL = TopicModel.TcModel()
                MODEL.train(path=path,num_topics=int(num_topics),iterations=int(iter),n_gram=ngram,lemmatization=lemma,stop_words=sw,tfidf=tfidf,model=model)
                QW.pwindow.close()
                notionUI.QMessageBox.information(QW,'Message','Train Successfully',notionUI.QMessageBox.Ok)
                QW.statusBar().showMessage('Current model: {}'.format(model))

def load_model(QW):
    global MODEL
    filewindow = notionUI.FileWindow()
    filewindow.setWindowTitle('choose model')
    if filewindow.exec_():
        if filewindow.path == '':
            notionUI.QMessageBox.warning(filewindow, 'Message', 'Please choose a folder.',
                                notionUI.QMessageBox.Ok, notionUI.QMessageBox.Ok)
        else:
            try:
                MODEL = TopicModel.TcModel()
                MODEL.load(filewindow.path)
            except:
                notionUI.QMessageBox.warning(filewindow,'Message','There is no model in the fold, please choose another folder.',notionUI.QMessageBox.Ok,notionUI.QMessageBox.Ok)
                return
            QW.statusBar().showMessage('Current model: {}'.format(filewindow.path.split('/')[-1]))
            notionUI.QMessageBox.information(QW, 'Message', 'Load Successfully', UI.QMessageBox.Ok)

def save_model(QW):
    global MODEL
    QW.filewindow = notionUI.FileWindow()
    QW.filewindow.setWindowTitle('choose folder')
    if QW.filewindow.exec_():
        MODEL.save(QW.filewindow.path)
        QW.filewindow.close()
        notionUI.QMessageBox.information(QW, 'Message', 'save successfully', notionUI.QMessageBox.Ok,
                        notionUI.QMessageBox.Ok)

def view_model(QW):
    viewindow = notionUI.ViewWindow()
    viewindow.show()

def update_model(QW):
    global MODEL
    filewindow = notionUI.FileWindow()
    filewindow.setWindowTitle('Choose training data')
    if filewindow.exec_():
        if filewindow.path == '':
            notionUI.QMessageBox.warning(QW, 'Message', 'Please choose a folder.', notionUI.QMessageBox.Ok, notionUI.QMessageBox.Ok)
        else:
            path = filewindow.path

            trainwindow = notionUI.TrainWindow()
            trainwindow.m_bt = notionUI.QLabel(MODEL.model_name)
            if trainwindow.exec_():
                model = trainwindow.m_bt.currentText().lower()
                iter = trainwindow.le1.text()
                topic_num = trainwindow.le2.text()
                ngram = trainwindow.c1.isChecked()
                lemma = trainwindow.c2.isChecked()
                sw = trainwindow.c3.isChecked()
                tfidf = trainwindow.c4.isChecked()

                if not json_to_csv(path):
                    notionUI.QMessageBox.warning(filewindow, 'Waring',
                                           'There is no training data, please choose another folder')
                    return
                else:
                    pwindow = notionUI.ProgressWindow()
                    pwindow.exec_()
                    MODEL = TCmodel.TcModel()
                    MODEL.update(path=path,num_topics=int(topic_num), iterations=int(iter), n_gram=ngram, lemmatization=lemma, stop_words=sw,
                                tfidf=tfidf, model=model)
                    pwindow.close()
                    notionUI.QMessageBox.information(QW, 'Message', 'Update Model Successfully', notionUI.QMessageBox.Ok)
                    QW.statusBar().showMessage('Current model: {}'.format(model))




if __name__ == '__main__':
    app = notionUI.QApplication(sys.argv)
    root = notionUI.Root()
    root.show()
    sys.exit(app.exec_())