
const PLAYFIELD_WIDTH = 300;
const SCREEN_HEIGHT = 600;

class Cannon {
    constructor() {
        this.width = 40;
        this.height = 16;

        this.x = Math.floor(
            PLAYFIELD_WIDTH / 2 - this.width / 2
        );

        this.y = SCREEN_HEIGHT - this.height - 20;

        this.speed = 6;
    }

    moveLeft() {
        this.x -= this.speed;

        if (this.x < 0) {
            this.x = 0;
        }
    }

    moveRight() {
        this.x += this.speed;

        if (this.x > PLAYFIELD_WIDTH - this.width) {
            this.x = PLAYFIELD_WIDTH - this.width;
        }
    }

    getShotPosition() {
        return [
            this.x + Math.floor(this.width / 2),
            this.y
        ];
    }
}

module.exports = Cannon;
