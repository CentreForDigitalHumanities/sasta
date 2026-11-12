import { MethodCategory } from './methodcategory';

export interface Method {
    id: number;
    name: string;
    category: MethodCategory;
    content: File | { name: string };
    date_added?: Date;
}
