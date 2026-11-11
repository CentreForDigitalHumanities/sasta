import { ListedTranscript } from './transcript';

export interface ListedCorpus {
    id?: number;
    name: string;
    method_category: number;
    num_transcripts: number;
    username?: string;
    date_added?: Date;
}

export interface Corpus extends Omit<ListedCorpus, 'num_transcripts'> {
    status: 'created';
    date_modified?: Date;
    default_method?: number;
    transcripts?: ListedTranscript[];
}
