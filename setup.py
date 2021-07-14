from setuptools import setup


with open("README.md", "r", encoding="utf8") as f:
    long_description = f.read()

setup(
    name="wechatpayv3",
    version="1.0.4",
    author="minibear",
    description="微信支付接口V3版python库(python sdk for wechatpay v3)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="BSD",
    keywords="python sdk wechatpay api v3 微信支付",
    url="https://github.com/minibear2021/wechatpayv3",
    packages=["wechatpayv3"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    install_requires=["requests>=2.21.0", "cryptography>=2.2.2"],
)
