class TicTacToe {
    constructor(prune = true) {
        this.board = [
            ['_', '_', '_'],
            ['_', '_', '_'],
            ['_', '_', '_']
        ];
        this.playerTurn = 'X';
        this.prune = prune;
        this.gamesEvaluated = 0;
        this.messageEl = document.getElementById("message");
        this.cells = document.querySelectorAll(".cell");
        this.bindEvents();
    }

    bindEvents() {
        this.cells.forEach(cell => {
            cell.addEventListener("click", () => {
                const x = parseInt(cell.dataset.x);
                const y = parseInt(cell.dataset.y);
                if (this.board[x][y] === '_' && this.playerTurn === 'X') {
                    this.board[x][y] = 'X';
                    cell.textContent = 'X';
                    if (!this.checkGameOver()) {
                        this.playerTurn = 'O';
                        setTimeout(() => this.aiMove(), 200);
                    }
                }
            });
        });

        document.getElementById("reset").addEventListener("click", () => this.reset());
    }

    checkGameOver() {
        const winner = this.gameOver();
        if (winner) {
            this.messageEl.textContent = winner === '_' ? "Tie!" : `${winner} wins!`;
            return true;
        }
        return false;
    }

    gameOver() {
        const b = this.board;
        for (let i=0;i<3;i++) {
            if (b[i][0]===b[i][1] && b[i][1]===b[i][2] && b[i][0]!=='_') return b[i][0];
            if (b[0][i]===b[1][i] && b[1][i]===b[2][i] && b[0][i]!=='_') return b[0][i];
        }
        if (b[0][0]===b[1][1] && b[1][1]===b[2][2] && b[0][0]!=='_') return b[0][0];
        if (b[0][2]===b[1][1] && b[1][1]===b[2][0] && b[0][2]!=='_') return b[0][2];
        if (b.flat().every(c => c!=='_')) return '_';
        return null;
    }

    aiMove() {
        this.gamesEvaluated = 0;
        const [_, x, y] = this.minimaxMax(-Infinity, Infinity, 0);
        if (x!==null && y!==null) {
            this.board[x][y] = 'O';
            document.querySelector(`.cell[data-x='${x}'][data-y='${y}']`).textContent = 'O';
        }
        this.messageEl.textContent = `AI evaluated ${this.gamesEvaluated} game states.`;

        // ✅ Only switch turn if game not over
        if (!this.checkGameOver()) {
            this.playerTurn = 'X';
        }
    }

    minimaxMax(alpha, beta, depth) {
        const winner = this.gameOver();
        if (winner) {
            this.gamesEvaluated++;
            if (winner==='X') return [-10 + depth, null, null];
            if (winner==='O') return [10 - depth, null, null];
            if (winner==='_') return [0, null, null];
        }

        let maxScore = -Infinity, maxMove = [null,null];
        for (let i=0;i<3;i++){
            for (let j=0;j<3;j++){
                if (this.board[i][j]==='_') {
                    this.board[i][j] = 'O';
                    let [score] = this.minimaxMin(alpha, beta, depth+1);
                    this.board[i][j] = '_';
                    if (score > maxScore) { maxScore = score; maxMove = [i,j]; }
                    alpha = Math.max(alpha,maxScore);
                    if (this.prune && maxScore>=beta) return [maxScore, ...maxMove];
                }
            }
        }
        return [maxScore, ...maxMove];
    }

    minimaxMin(alpha, beta, depth) {
        const winner = this.gameOver();
        if (winner) {
            this.gamesEvaluated++;
            if (winner==='X') return [-10 + depth, null, null];
            if (winner==='O') return [10 - depth, null, null];
            if (winner==='_') return [0, null, null];
        }

        let minScore = Infinity, minMove = [null,null];
        for (let i=0;i<3;i++){
            for (let j=0;j<3;j++){
                if (this.board[i][j]==='_') {
                    this.board[i][j] = 'X';
                    let [score] = this.minimaxMax(alpha, beta, depth+1);
                    this.board[i][j] = '_';
                    if (score < minScore) { minScore = score; minMove = [i,j]; }
                    beta = Math.min(beta,minScore);
                    if (this.prune && minScore<=alpha) return [minScore, ...minMove];
                }
            }
        }
        return [minScore, ...minMove];
    }

    reset() {
        this.board = [['_','_','_'],['_','_','_'],['_','_','_']];
        this.playerTurn = 'X';
        this.cells.forEach(c => c.textContent='');
        this.messageEl.textContent = '';
    }
}

const game = new TicTacToe(true);
