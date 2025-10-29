import { ListedTranscript } from './transcript';

export interface ListedCorpus {
    id?: number;
    name: string;
    method_category: number;
    num_transcripts: number;
    username?: string;
}

export interface Corpus extends Omit<ListedCorpus, 'num_transcripts'> {
    date_added?: Date;
    date_modified?: Date;
    default_method?: number;
    transcripts?: ListedTranscript[];
    share_permissions: boolean;
}
