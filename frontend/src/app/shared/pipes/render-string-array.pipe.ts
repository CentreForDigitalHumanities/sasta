import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
    name: 'renderStringArray',
})
export class RenderStringArrayPipe implements PipeTransform {
    transform(value: string | string[], ..._args: unknown[]): unknown {
        if (value instanceof Array) {
            return value.join(', ');
        }
        return value;
    }
}
