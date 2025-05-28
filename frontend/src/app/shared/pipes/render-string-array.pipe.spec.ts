import { RenderStringArrayPipe } from './render-string-array.pipe';

describe('RenderStringArrayPipe', () => {
    it('create an instance', () => {
        const pipe = new RenderStringArrayPipe();
        expect(pipe).toBeTruthy();
    });

    it('should join array of strings with comma and space', () => {
        const pipe = new RenderStringArrayPipe();
        const result = pipe.transform(['apple', 'banana', 'cherry']);
        expect(result).toBe('apple, banana, cherry');
    });

    it('should return the string as is if input is a string', () => {
        const pipe = new RenderStringArrayPipe();
        const result = pipe.transform('singleString');
        expect(result).toBe('singleString');
    });

    it('should return an empty string when given an empty array', () => {
        const pipe = new RenderStringArrayPipe();
        const result = pipe.transform([]);
        expect(result).toBe('');
    });

    it('should handle array with one element', () => {
        const pipe = new RenderStringArrayPipe();
        const result = pipe.transform(['onlyOne']);
        expect(result).toBe('onlyOne');
    });
});
