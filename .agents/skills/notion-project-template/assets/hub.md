<columns>
	<column ratio="25">
		## NAVIGATION {color="blue_bg"}
		<page url="{{page.project}}" color="blue">프로젝트 관리</page>
		- <mention-page url="{{record.guide}}"/>
		- <mention-page url="{{page.dashboard}}"/>
		- <mention-page url="{{page.my_tasks}}"/>
		- <mention-page url="{{page.sprint}}"/>
		- <mention-page url="{{page.timeline}}"/>
		<page url="{{page.communication}}" color="blue">커뮤니케이션</page>
		- <mention-page url="{{page.meetings}}"/>
		<page url="{{page.planning}}" color="blue">기획</page>
		- <mention-page url="{{page.requirements}}"/>
		- <mention-page url="{{page.ai}}"/>
		<page url="{{page.development}}" color="blue">개발</page>
		- <mention-page url="{{page.frontend}}"/>
		- <mention-page url="{{page.backend}}"/>
		- <mention-page url="{{page.dev_docs}}"/>
		<page url="{{page.design}}" color="blue">디자인</page>
		- <mention-page url="{{page.figma}}"/>
		<page url="{{page.resources}}" color="blue">자료</page>
		- <mention-page url="{{page.shortcuts}}"/>
		- <mention-page url="{{page.dev_resources}}"/>
		- <mention-page url="{{page.business_resources}}"/>
		- <mention-page url="{{page.learning}}"/>
		<page url="{{page.database}}">DATABASE</page>
	</column>
	<column ratio="75">
		## {{project_name}} 프로젝트 보드 {color="blue_bg"}
		<database url="{{linked.root.0}}" inline="true" data-source-url="collection://{{ds.Tasks}}"></database>
	</column>
</columns>
