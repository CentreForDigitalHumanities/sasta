from annotations.utils import preflabel
from sastadev.SAFreader import (commentsheaders, levelheaders, literallevels,
                                speakerheaders, stagesheaders,
                                unalignedheaders, uttidheaders)

SAF_COMMENT_LEVEL = preflabel(commentsheaders, str.capitalize)
SAF_COMMENT_COLUMN = preflabel(commentsheaders, str.capitalize)
SAF_COMMENT_HEADERS = list(map(str.lower, commentsheaders))

SAF_UTT_HEADER = SAF_UTT_LEVEL = preflabel(uttidheaders, str.capitalize)
SAF_UTT_LEVELS = list(map(str.lower, uttidheaders))

SAF_UNALIGNED_LEVEL = preflabel(unalignedheaders, str.capitalize)
SAF_UNALIGNED_LEVELS = list(map(str.lower, unalignedheaders))

SAF_LEVEL_HEADER = preflabel(levelheaders, str.capitalize)
SAF_LEVEL_HEADERS = list(map(str.lower, levelheaders))

SAF_FASES_COLUMN = preflabel(stagesheaders, str.capitalize)
SAF_FASES_HEADERS = list(map(str.lower, stagesheaders))

SAF_SPEAKER_HEADER = preflabel(speakerheaders, str.capitalize)
SAF_SPEAKER_COLUMNS = list(map(str.lower, speakerheaders))

SAF_LITERAL_LEVELS = list(map(str.lower, literallevels))

# Composed headers
PRE_WORDS_HEADERS = [SAF_UTT_HEADER, SAF_LEVEL_HEADER, SAF_UNALIGNED_LEVEL]
POST_WORDS_HEADERS = [SAF_FASES_COLUMN, SAF_COMMENT_COLUMN]

PRIMARY_COLOR = '3f51b5'
SECONDARY_COLOR = 'b5a33f'
