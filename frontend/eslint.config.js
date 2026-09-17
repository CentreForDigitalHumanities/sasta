// @ts-check
const tsParser = require('@typescript-eslint/parser');
const tsPlugin = require('@typescript-eslint/eslint-plugin');
const angularPlugin = require('@angular-eslint/eslint-plugin');
const angularTemplatePlugin = require('@angular-eslint/eslint-plugin-template');
const angularTemplateParser = require('@angular-eslint/template-parser');
const eslintJs = require('@eslint/js');

// @typescript-eslint flat/recommended rules (eslint overrides + TS-specific rules)
const tsRecommendedRules = {
    ...tsPlugin.configs['flat/recommended'][1].rules,
    ...tsPlugin.configs['flat/recommended'][2].rules,
};

module.exports = [
    {
        ignores: ['projects/**/*'],
    },
    {
        files: ['**/*.ts'],
        languageOptions: {
            parser: tsParser,
            parserOptions: {
                project: ['tsconfig.json'],
                createDefaultProgram: true,
            },
        },
        plugins: {
            '@typescript-eslint': tsPlugin,
            '@angular-eslint': angularPlugin,
        },
        processor: angularTemplatePlugin.processors['extract-inline-html'],
        rules: {
            ...eslintJs.configs.recommended.rules,
            ...tsRecommendedRules,
            ...angularPlugin.configs.recommended.rules,
            // New v20 rules not applicable to this non-standalone/constructor-injection project
            '@angular-eslint/prefer-standalone': 'off',
            '@angular-eslint/prefer-inject': 'off',
            '@typescript-eslint/no-unused-vars': [
                'error',
                { argsIgnorePattern: '^_' },
            ],
            '@angular-eslint/component-selector': [
                'error',
                {
                    prefix: 'sas',
                    style: 'kebab-case',
                    type: 'element',
                },
            ],
            '@angular-eslint/directive-selector': [
                'error',
                {
                    prefix: 'sas',
                    style: 'camelCase',
                    type: 'attribute',
                },
            ],
            '@typescript-eslint/naming-convention': [
                'error',
                {
                    selector: 'default',
                    format: ['camelCase'],
                    leadingUnderscore: 'allow',
                    trailingUnderscore: 'allow',
                },
                {
                    selector: 'enumMember',
                    format: ['camelCase', 'UPPER_CASE'],
                },
                {
                    selector: 'property',
                    format: ['camelCase', 'snake_case'],
                    leadingUnderscore: 'allow',
                },
                {
                    selector: 'classProperty',
                    format: ['camelCase', 'PascalCase'],
                    leadingUnderscore: 'allow',
                },
                {
                    selector: 'variable',
                    format: ['camelCase', 'UPPER_CASE'],
                    leadingUnderscore: 'allow',
                    trailingUnderscore: 'allow',
                },
                {
                    selector: 'typeLike',
                    format: ['PascalCase'],
                },
            ],
            '@typescript-eslint/explicit-module-boundary-types': [
                'error',
                {
                    allowArgumentsExplicitlyTypedAsAny: true,
                    allowDirectConstAssertionInArrowFunctions: true,
                    allowHigherOrderFunctions: false,
                    allowTypedFunctionExpressions: true,
                    allowedNames: [
                        'ngOnInit',
                        'ngOnDestroy',
                        'ngAfterViewInit',
                        'ngOnChanges',
                    ],
                },
            ],
            '@typescript-eslint/typedef': 'error',
            'dot-notation': 'error',
            'id-denylist': [
                'error',
                'any',
                'Number',
                'number',
                'String',
                'string',
                'Boolean',
                'boolean',
                'Undefined',
                'undefined',
            ],
            'indent': ['error', 4, { SwitchCase: 1 }],
            'no-empty-function': 'off',
            'no-shadow': 'error',
            'no-unused-expressions': 'error',
            'no-use-before-define': 'off',
            'quotes': [
                'error',
                'single',
                {
                    avoidEscape: true,
                    allowTemplateLiterals: true,
                },
            ],
            'semi': 'error',
            'no-underscore-dangle': 'off',
        },
    },
    {
        files: ['**/*.html'],
        languageOptions: {
            parser: angularTemplateParser,
        },
        plugins: {
            '@angular-eslint/template': angularTemplatePlugin,
        },
        rules: {
            ...angularTemplatePlugin.configs.recommended.rules,
            '@angular-eslint/template/eqeqeq': 'error',
        },
    },
];
