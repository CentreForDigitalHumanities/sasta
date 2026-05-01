import { Component, Input } from '@angular/core';
import {
    faCheck,
    faMinus,
    faProjectDiagram,
    faSearch,
    IconDefinition,
} from '@fortawesome/free-solid-svg-icons';
import _ from 'lodash';
import { Transcript, Utterance } from '@models';

@Component({
    standalone: false,
    selector: 'sas-utterances-list',
    templateUrl: './utterances-list.component.html',
    styleUrls: ['./utterances-list.component.scss'],
})
export class UtterancesListComponent {
    @Input()
    set transcript(transcript: Transcript) {
        this.sortedUtterances = _.sortBy(transcript.utterances, (t) => t.uttno);
    }
    faCheck = faCheck;
    faMinus = faMinus;
    faSearch = faSearch;
    faProjectDiagram = faProjectDiagram;

    sortedUtterances: Utterance[];
    loadingTree = false;

    treeSentence?: string;
    treeXml?: string;

    constructor() {}

    analysisIcon(u: Utterance): IconDefinition {
        return u.for_analysis ? faCheck : faMinus;
    }

    showTree(utterance: Utterance): void {
        this.loadingTree = true;
        this.treeSentence = utterance.sentence;
        this.treeXml = utterance.parse_tree;
        this.loadingTree = false;
    }

    onCloseTree(): void {
        this.loadingTree = false;
        this.treeSentence = undefined;
        this.treeXml = undefined;
    }
}
