#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <opencv2/core.hpp>

namespace Ui {
class MainWindow;
}

namespace cv {
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
    cv::Rect m_chop;
    cv::Mat m_cvFrame;
    QImage *m_displayImg;
    cv::VideoCapture *m_cap;
    int m_width, m_height, m_imgWidth;
    float m_leftP, m_rightP, m_bottomP, m_topP;

    Ui::MainWindow *ui;
};

#endif // MAINWINDOW_H
