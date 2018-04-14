#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>

namespace Ui {
class MainWindow;
}

namespace cv {
class Mat;
class VideoCapture;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow( QWidget *parent = 0 );
    ~MainWindow();

protected:
    void timerEvent( QTimerEvent * );

private slots:
    void on_pushButton_clicked();

private:
    cv::Mat *m_cvFrame;
    QImage *m_displayImg;
    int m_width, m_height;
    cv::VideoCapture *m_cap;
    float m_leftP, m_rightP, m_bottomP, m_topP;

    Ui::MainWindow *ui;
};

#endif // MAINWINDOW_H
