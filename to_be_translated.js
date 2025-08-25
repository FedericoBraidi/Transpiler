function func (x, y) {
    if (x === 10) {
        console.log('Variable x is 10.');
    }
    else{
        if (y === 3) {
            console.log('Variable x is not 10 but variable y is 3.');
        }
        else{
            console.log('Variable x is not 10 and variable y is not 3.');
            return 1;
        }
    }
}

var x=10;
var y=2;
console.log(func(x,y));
