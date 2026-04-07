import { TaskStatus } from './task';

export interface AnalysisRun {
    id: number;
    created: Date;
    annotation_file: string;
    method: number;
    is_manual_correction: boolean;
    task_id?: string | null;
    task_status?: TaskStatus | null;
    results_available: boolean;
}

export interface Utterance {
    id: number;
    sentence: string;
    speaker: string;
    utt_id?: number;
    uttno: number;
    xsid?: number;
    for_analysis: boolean;
    parse_tree: string;
}

// eslint-disable-next-line no-shadow
export enum TranscriptStatus {
    UNKNOWN,
    CREATED,
    CONVERTING,
    CONVERTED,
    CONVERSION_FAILED,
    PARSING,
    PARSED,
    PARSING_FAILED,
}

export interface ListedTranscript {
    id?: number;
    name: string;
    status: number;
    status_name:
        | 'unknown'
        | 'created'
        | 'converting'
        | 'converted'
        | 'conversion-failed'
        | 'parsing'
        | 'parsed'
        | 'parsing-failed';
    date_added?: Date;
    corpus: number;
    utterances: number[];
}

export interface Transcript extends Omit<ListedTranscript, 'utterances'> {
    content: string;
    parsed_content: string;
    corrected_content: string;
    utterances: Utterance[];
    latest_run?: AnalysisRun;
    latest_corrections?: AnalysisRun;
    target_speakers?: string;
}
