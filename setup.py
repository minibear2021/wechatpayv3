from setuptools import setup


with open("README.md", "r", encoding="utf8") as f:
    long_description = f.read()

setup(
    name="wechatpayv3",
    version="1.3.11",
    author="minibear",
    author_email="321983@qq.com",
    description="微信支付 Python SDK(python sdk for wechatpay)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    keywords="python sdk wechatpay api v3 微信支付",
    url="https://github.com/minibear2021/wechatpayv3",
    packages=["wechatpayv3"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Office/Business :: Financial",
        "Programming Language :: Python :: 3",
    ],
    install_requires=["requests>=2.21.0", "cryptography>=35.0.0"],
)
