<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0">

    <!-- This stylesheet transforms the ODIN version of the HBB  model to RDF-->


    <xsl:template match="igt/example">
        
        <xsl:apply-templates select="goldConcept"/>
        <xsl:apply-templates select="language"/>
        <xsl:apply-templates select="source"/>
        <xsl:apply-templates select="item"/>
        <xsl:text>&#10;</xsl:text>
        
        <xsl:apply-templates select="interlinear-text/phrases/phrase"/>
    </xsl:template>



    <xsl:template match="goldConcept">
        <xsl:value-of select="."/>
        <xsl:text> &#10;</xsl:text>
    </xsl:template>

    <xsl:template match="language">
        <xsl:value-of select="@code"/>
        <xsl:text> &#10;</xsl:text>
    </xsl:template>


    <xsl:template match="source">
        <xsl:value-of select="."/>
        <xsl:text> &#10;</xsl:text>
    </xsl:template>
    
    <xsl:template match="item">
            <xsl:value-of select="."/>
    </xsl:template>

    <xsl:template match="interlinear-text/phrases/phrase">
         <xsl:for-each select="words/word">
                <xsl:apply-templates select="item"/>
             <xsl:text>&#9;</xsl:text>                       
         </xsl:for-each>        
        <xsl:text>&#10;</xsl:text>
        
        <!-->Now build line 2</-->
        
        <xsl:for-each select="words/word">
            <xsl:call-template name="build-line-2">
                <xsl:with-param name="word_value" select="item"/>
            </xsl:call-template>
        </xsl:for-each>        
        <xsl:text>&#10;</xsl:text>
        


        <!-->Now grab the translation line<-->
        
        <xsl:apply-templates select="item"/>
        
    </xsl:template>

    <!--template for building line 2-->
    <xsl:template name="build-line-2">
        <!-- param is currently not used -->
        <xsl:param name="word_value"/>
        

         <xsl:for-each select="morphemes/morph/item">
            <xsl:if test="@type!='text'">
                <xsl:value-of select="replace(.,'-','.')"/>
                <xsl:if test="position() != last()">
                    <xsl:text>-</xsl:text>
                </xsl:if>
                <xsl:if test="position() = last()">
                    <xsl:text> </xsl:text>
                </xsl:if>
               
            </xsl:if>
        </xsl:for-each>
        <xsl:text> </xsl:text>
        
        
    </xsl:template>


</xsl:stylesheet>
