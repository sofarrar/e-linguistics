<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0"
                       xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
                       xmlns:ldx="lingdata.xsd">
    <xsl:output method="xml" version="1.0" encoding="UTF-8" indent="yes" />
    
    <!-- Main routine -->
    <xsl:template match="/igt">
        <xsl:element name="rdf:RDF">
            <xsl:attribute namespace="http://www.w3.org/1999/02/22-rdf-syntax-ns#" name="noNamespaceSchemaLocation">http://www.w3.org/2001/04/infoset</xsl:attribute>
            <xsl:attribute name="ns01" namespace="lingdata.xsd">ns1</xsl:attribute>
            <xsl:text>&#10;</xsl:text>
            <xsl:for-each select="triple">
                <xsl:text>&#10;</xsl:text>
                <xsl:call-template name="phrase2words" />
                <xsl:text>&#10;&#10;</xsl:text>
                <xsl:call-template name="word2morphemes" />
            </xsl:for-each>
        </xsl:element>
    </xsl:template>
    
    <!-- Template for listing the constituent words of a phrase -->
    <xsl:template name="phrase2words">
        <xsl:element name="rdf:Description">
            <xsl:attribute name="about" select="child::node()[2]/text()"></xsl:attribute>
            <xsl:element name="hasConstituent">
                <xsl:element name="rdf:Seq">
                    <xsl:for-each select="clause/synword">
                        <xsl:element name="ldx:synword">
                            <xsl:call-template name="reconstructWord" />
                        </xsl:element>
                    </xsl:for-each>
                </xsl:element>
            </xsl:element>
        </xsl:element>
    </xsl:template>
    
    <!-- Template for listing the constituent morphemes of a word. -->
    <xsl:template name="word2morphemes">
        <xsl:for-each select="clause/synword">
            <xsl:element name="rdf:Description">
                <xsl:attribute name="about">
                    <xsl:call-template name="reconstructWord" />
                </xsl:attribute>
                <xsl:element name="hasConstituent">
                    <xsl:element name="rdf:Seq">
                        <xsl:for-each select="morpheme">
                            <xsl:element name="ldx:morpheme">
                                <xsl:value-of>
                                    <xsl:variable name="uid" select="./@representation" />
                                    <xsl:for-each select="preceding::node()">
                                        <xsl:if test="@id=$uid">
                                            <xsl:value-of select="text()" />
                                        </xsl:if>
                                    </xsl:for-each>
                                </xsl:value-of>
                            </xsl:element>
                        </xsl:for-each>
                    </xsl:element>
                </xsl:element>
            </xsl:element>
            <xsl:text>&#10;&#10;</xsl:text>
        </xsl:for-each>
    </xsl:template>
    
    <!-- Template subroutine to make source words with hyphens
                built from individual morphemes -->
    <xsl:template name="reconstructWord">
        <xsl:for-each select="morpheme">
            <xsl:variable name="prevNode" select="preceding-sibling::node()/@gloss"></xsl:variable>
            <xsl:variable name="uid" select="./@representation" />
            <xsl:for-each select="preceding::node()">
                <xsl:if test="@id=$uid">
                    <xsl:if test="$prevNode">
                        <xsl:text>-</xsl:text>
                    </xsl:if>
                    <xsl:value-of select="text()" />
                </xsl:if>
            </xsl:for-each>
        </xsl:for-each>
    </xsl:template>
</xsl:stylesheet>
