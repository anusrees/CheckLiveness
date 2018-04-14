#include "mainwindow.h"
#include "ui_mainwindow.h"

#include <string>
#include <assert.h>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>

void setDisplayImg( QImage *displayImg, cv::Mat cvFrame,
                    int width, int height )
{
    int cvIndex = 0;
    unsigned char red, green, blue;

    for( int y = 0; y < height; y++ )
    {
        for( int x = 0; x < width; x++ )
        {
            red   = cvFrame.data[cvIndex+2];
            green = cvFrame.data[cvIndex+1];
            blue  = cvFrame.data[cvIndex+0];

            displayImg->setPixel( x, y, qRgb( red, green, blue ));
            cvIndex += 3;
        }
    }
}

MainWindow::MainWindow( QWidget *parent ) :
    QMainWindow( parent ),
    ui( new Ui::MainWindow )
{
    m_leftP   = 0;
    m_topP    = 0;
    m_rightP  = 1;
    m_bottomP = 1;

    m_cap = new cv::VideoCapture( 0 );
    assert( m_cap->isOpened());
    m_cap->read( m_cvFrame );

    m_width    = ( m_rightP-m_leftP )*m_cvFrame.cols;
    m_height   = ( m_bottomP-m_topP )*m_cvFrame.rows;
    m_imgWidth = m_cvFrame.cols;

    m_chop.x = m_leftP*m_cvFrame.cols;
    m_chop.y = m_topP*m_cvFrame.rows;

    m_chop.width  = m_width;
    m_chop.height = m_height;

    m_cvFrame = m_cvFrame( m_chop );
    m_cvFrame = m_cvFrame.clone();

    m_displayImg = new QImage( m_width, m_height,
                               QImage::Format_RGB32 );

    setDisplayImg( m_displayImg, m_cvFrame, m_width, m_height );

    ui->setupUi( this );
    ui->centralWidget->setFixedSize( QSize( m_width+20, m_height+10 ));
    ui->layoutWidget->setFixedSize( QSize( m_width, m_height ));
    ui->label_2->setPixmap( QPixmap::fromImage( *m_displayImg ));

    setFixedSize( sizeHint());

    startTimer( 1 );
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::timerEvent( QTimerEvent * )
{
    m_cap->read( m_cvFrame );
    m_cvFrame = m_cvFrame( m_chop );
    m_cvFrame = m_cvFrame.clone();

    setDisplayImg( m_displayImg, m_cvFrame, m_width, m_height );
    ui->label_2->setPixmap( QPixmap::fromImage( *m_displayImg ));
}

void MainWindow::on_pushButton_clicked()
{
    std::string str = ui->label->text().toStdString();

    if( str.compare( "LIVE" ) == 0 || str.compare( "" ) == 0 )
        ui->label->setText( QString( "SPOOF" ));
    else
        ui->label->setText( QString( "LIVE" ));
}
