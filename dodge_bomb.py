import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}  # 辞書の定義
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRect or 爆弾Rect
    戻り値：判定結果タプル（横、縦)（True：画面内/False：画面外）
    Rectオブジェクトのleft, right, top, bottomの値から画面内・外を判断する
    """
    # 横方向判定
    yoko, tate = True, True  # 横、縦方向用の変数
    if rct.left < 0 or WIDTH < rct.right:  # 画面外だったら
        yoko = False
    # 縦方向判定
    if rct.top < 0 or HEIGHT < rct.bottom:  # 画面外だったら
        tate = False
    return yoko, tate


def gameover(screen: pg.Surface) -> None:
    """
    引数：screen
    gameover画面の表示
    背景の黒い長方形、GameOverの文字、こうかとん画像枚を張り出す。
    """
    bk_img = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(bk_img, (0, 0, 0), (0, 0, 1100, 650))
    bk_img.set_alpha(177)  # 半透明化
    bk_rct = bk_img.get_rect()
    bk_rct.center = 550, 325
    screen.blit(bk_img, bk_rct) # 背景張り出し
    fonto = pg.font.Font(None, 80)  # 文字読み込み
    txt = fonto.render("Gameover", True, (255, 255, 255))
    screen.blit(txt, [400, 300])  # 文字張り出し
    kk1_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 1.5)  # こうかとん読み込み
    kk1_rct = kk1_img.get_rect() # Rect読み込み
    kk1_rct.center = 300, 325  # １枚目座標
    screen.blit(kk1_img, kk1_rct)
    kk1_rct.center = 800, 325  # ２枚目座標
    screen.blit(kk1_img, kk1_rct)
    pg.display.update()  # 再読み込み
    time.sleep(5)  # 時間ストップ


# def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:    
    

def main():


    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    # こうかとん初期化
    bg_img = pg.image.load("fig/pg_bg.jpg")  
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    # 爆弾初期化
    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    bb_img.set_colorkey((0, 0, 0))
    vx, vy = +5, +5
    clock = pg.time.Clock()
    tmr = 0
    # bb_accs = [a for a in range(1, 11)]

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        # こうかとんRectと爆弾Rectが重なっていたら
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]  # 左右方向
                sum_mv[1] += mv[1]  # 上下方向
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True,True):  # 画面外だったら
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])  #画面内に戻す
        bb_rct.move_ip(vx, vy) #爆弾の移動
        yoko, tate = check_bound(bb_rct)
        if not yoko:  # 左右どちらかにはみ出ていたら
            vx *= -1
        if not tate:  # 上下どちらかにはみ出ていたら
            vy *= -1
        screen.blit(kk_img, kk_rct)
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)




if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
