import React from 'react';
import bem, {makeBem} from 'js/bem';
import {getFlatQuestionsList} from 'js/assetUtils';
import type {FlatQuestion} from 'js/assetUtils';
import type {
  AssetContent,
  SubmissionResponse,
} from 'js/dataInterface';
import {getRowData} from 'js/components/submissions/submissionUtils';
import './submissionDataList.scss';

bem.SubmissionDataList = makeBem(null, 'submission-data-list', 'ul');
bem.SubmissionDataListQuestion = makeBem(null, 'submission-data-list-question', 'li');
bem.SubmissionDataListQuestion__path = makeBem(bem.SubmissionDataListQuestion, 'path');
bem.SubmissionDataListQuestion__label = makeBem(bem.SubmissionDataListQuestion, 'label', 'h3');
bem.SubmissionDataListQuestion__response = makeBem(bem.SubmissionDataListQuestion, 'response');

interface SubmissionDataListProps {
  assetContent: AssetContent;
  submissionData: SubmissionResponse;
  /** A list of questions that should be omitted from display. */
  hideQuestions?: string[]
  /** Whether to display the path (the groups) or not. */
  hideGroups?: boolean
}

interface SubmissionDataListState {}

export default class SubmissionDataList extends React.Component<
  SubmissionDataListProps,
  SubmissionDataListState
> {
  constructor(props: SubmissionDataListProps) {
    super(props);
    this.state = {};
  }

  renderQuestion(question: FlatQuestion) {
    // check if the question shouldn't be hidden
    if (
      Array.isArray(this.props.hideQuestions) &&
      this.props.hideQuestions.includes(question.name)
    ) {
      return null;
    }

    const response = getRowData(
      question.name,
      this.props.assetContent.survey || [],
      this.props.submissionData
    );

    return (
      <bem.SubmissionDataListQuestion key={question.name}>
        {!this.props.hideGroups && question.parents.length >= 1 &&
          <bem.SubmissionDataListQuestion__path>
            {question.parents.join(' / ')}
          </bem.SubmissionDataListQuestion__path>
        }

        <bem.SubmissionDataListQuestion__label>
          {question.label}
        </bem.SubmissionDataListQuestion__label>

        <bem.SubmissionDataListQuestion__response>
          {response ? response : t('N/A')}
        </bem.SubmissionDataListQuestion__response>
      </bem.SubmissionDataListQuestion>
    );
  }

  render() {
    if (!this.props.assetContent.survey) {
      return null;
    }

    const items = getFlatQuestionsList(this.props.assetContent.survey, 0);

    return (
      <bem.SubmissionDataList>
        {items.map(this.renderQuestion.bind(this))}
      </bem.SubmissionDataList>
    );
  }
}
