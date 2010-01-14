<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0">
<xsl:output method="xml" version="1.0" encoding="UTF-8" indent="yes" />

<!-- Main routine
            for each example in the source document,
            gets the native orthography line, gloss line,
            and sets up the clause sturcture as well. -->
    
    <xsl:template match="/igt">
        <xsl:element name="igt">
            <xsl:attribute  namespace="http://www.w3.org/2001/XMLSchema-instance" name="xsi:schemaLocation">http://www.linguistics-ontology.org/schemas/2008 igt.xsd</xsl:attribute>
            <xsl:for-each select="example">
                <xsl:text>&#10;&#10;</xsl:text>
                <xsl:element name="igt_example">
                    <xsl:text>&#10;&#10;</xsl:text>
                    <xsl:call-template name="make-source-line" />
                    <xsl:call-template name="make-source-morphemes" />
                    <xsl:text>&#10;&#10;</xsl:text>
                    <xsl:call-template name="make-trans-line" />
                    <xsl:text>&#10;&#10;</xsl:text>
                    <xsl:call-template name="make-gloss-clause" />
                    <xsl:call-template name="make-trans-ref" />
                </xsl:element>
            </xsl:for-each>
        </xsl:element>
    </xsl:template>
    
    <!-- template for identifying all the parts of the source line -->
        <xsl:template name="make-source-line">
              <xsl:element name="representation">
                <xsl:attribute name="type">orthographic</xsl:attribute>
                <xsl:attribute name="id" select="generate-id(.)" />
                <xsl:for-each select="interlinear-text/phrases/phrase/words/word/item">
                    <xsl:copy-of select="text()" />
                    <xsl:text> </xsl:text>
                </xsl:for-each>
            </xsl:element>
        </xsl:template>
    
    <!-- template for creating representation lines for
                source morphemes, which are selected by type="text"-->
        <xsl:template name="make-source-morphemes">
            <xsl:for-each select="interlinear-text/phrases/phrase/words/word/morphemes/morph">
                <xsl:element name="representation">
                    <xsl:attribute name="type">orthographic</xsl:attribute>
                    <xsl:attribute name="id" select="generate-id(.)" />
                    <xsl:for-each select="item">
                        <xsl:if test="@type='text'">
                            <xsl:copy-of select="text()" />
                        </xsl:if>
                    </xsl:for-each>
                </xsl:element>
            </xsl:for-each>
        </xsl:template>
    
<!-- template for grabbing the gloss line and putting it in a representation line -->    
        <xsl:template name="make-trans-line">
             <xsl:element name="representation">
                <xsl:attribute name="type">orthographic</xsl:attribute>
                 <xsl:attribute name="id" select="generate-id(./interlinear-text/phrases/phrase/item)" />
                <xsl:for-each select="interlinear-text/phrases/phrase/item">
                    <xsl:copy-of select="text()" />
                </xsl:for-each>
            </xsl:element>
        </xsl:template>

<!-- template to create a clause and its constituent synwords with morphemes -->
        <xsl:template name="make-gloss-clause">
             <xsl:element name="clause">
                <xsl:attribute name="representation" select="generate-id(.)" />
                <xsl:for-each select="interlinear-text/phrases/phrase/words/word">
                    <xsl:element name="synword">
                        <xsl:for-each select="morphemes/morph">
                            <xsl:element name="morpheme">
                                <xsl:attribute name="representation" select="generate-id(.)" />
                                <xsl:for-each select="item">
                                    <xsl:if test="@type='gloss'">
                                        <xsl:attribute name="gloss" select="text()" />
                                    </xsl:if>
                                    <xsl:if test="@type='gram'">
                                        <xsl:attribute name="gloss" select="text()"></xsl:attribute>
                                    </xsl:if>
                                </xsl:for-each>
                            </xsl:element>
                        </xsl:for-each>
                    </xsl:element>
                </xsl:for-each>
            </xsl:element>
            <xsl:text>&#10;&#10;</xsl:text>
        </xsl:template>
    
<!-- template that identifies id of source and target -->
    <xsl:template name="make-trans-ref">
             <xsl:element name="translation">
                <xsl:attribute name="source" select="generate-id(.)" />
                 <xsl:attribute name="target" select="generate-id(./interlinear-text/phrases/phrase/item)" />
             </xsl:element>
            <xsl:text>&#10;&#10;</xsl:text>        
        </xsl:template>

    </xsl:stylesheet>